#! /usr/bin/python
# -*- coding: utf-8 -*-

"""A simple game server for LAN."""

import time
import threading
import socket
import socketserver

from . import utils
from ..game.core import Game
from ..game.deck import Deck
from ..utils.message import info, warning

__author__ = 'fyabc'


class LanServer(socketserver.ThreadingTCPServer):
    """The server class."""

    # This server only support 2 users now.
    MaxUsers = 2

    def __init__(self, server_address, RequestHandlerClass, bind_and_activate=True):
        super().__init__(server_address, RequestHandlerClass, bind_and_activate=bind_and_activate)

        # The game to play.
        self.game = None

        # Users in this local network, contains game players (will add watchers in future).
        # Key: ``User`` instance
        # Value: user output fd
        self.users = {}

        # Lock for users in the network.
        self._user_lock = threading.Lock()

    def add_user(self, user, output_fd):
        with self._user_lock:
            if len(self.users) >= self.MaxUsers:
                raise utils.ClientError('Server full, cannot join this game!')
            elif user in self.users:
                raise utils.ClientError('{} already exists!'.format(user))
            self.users[user] = output_fd

    def remove_user(self, user):
        with self._user_lock:
            if user not in self.users:
                raise utils.ClientError('{} not in the network!'.format(user))
            del self.users[user]

    @property
    def game_started(self):
        with self._user_lock:
            return self.game is not None

    def broadcast(self, msg_type, obj, locked=True):
        if locked:
            with self._user_lock:
                for user, f_out in self.users.items():
                    utils.send_msg(f_out, msg_type, **obj)
        else:
            for user, f_out in self.users.items():
                utils.send_msg(f_out, msg_type, **obj)

    def broadcast_text(self, text, locked=True):
        self.broadcast('text', {'text': text}, locked=locked)

    def try_start_game(self):
        with self._user_lock:
            # If all users in, try to start the game.
            if len(self.users) < 2:
                return

            users = list(self.users.keys())
            users[0].player_id = 0
            users[1].player_id = 1

            self.game = Game()

            start_game_iter = self.game.start_game(
                decks=[
                    Deck.from_code(users[0].deck_code),
                    Deck.from_code(users[1].deck_code),
                ],
                mode='standard',
            )

            try:
                next(start_game_iter)
                start_game_iter.send([[], []])
            except StopIteration:
                pass

            self.broadcast_text('Game ({} vs {}) start!'.format(users[0].nickname, users[1].nickname), locked=False)
            self.broadcast('game_status', self.game.game_status(), locked=False)


class LanHandler(socketserver.StreamRequestHandler):
    """Handles the life cycle of a user's connection to the LAN server: connecting, playing games,
    and disconnecting.
    """

    def __init__(self, request, client_address, server):
        self.user = None

        super().__init__(request, client_address, server)

    def setup(self):
        super().setup()

    def handle(self):
        # 1. Ask user data from client.
        user_data = self.recv()
        assert user_data['type'] == 'user_data'
        self.user = utils.NetworkUser(self.client_address, user_data['nickname'], user_data['deck_code'])

        failed = False
        try:
            self.server.add_user(self.user, self.wfile)
            self.send_text('Hello {}, welcome to the HearthStone local server!'.format(self.user.nickname))
            self.broadcast_text('{} has joined into the game.'.format(self.user.nickname), False)
            info('{} has joined into the game.'.format(self.user.nickname))
            self.server.try_start_game()
        except utils.ClientError as e:
            self.send_text(e.args[0], error=True)
            failed = True
        except socket.error:
            failed = True

        if failed:
            return

        # 2. Wait for game start.
        while not failed and not self.server.game_started:
            try:
                # [NOTE] Need test here.
                self.send_text('Wait for game start!')
                time.sleep(1)
            except socket.error:
                failed = True

        # 3. Main game loop.
        while not failed:
            try:
                # todo: receive action; send game status after each action (of all users)
                self.send('game_status', **self.server.game.game_status())
                time.sleep(1)
            except socket.error:
                failed = True

    def finish(self):
        try:
            self.broadcast_text('{} has quit.'.format(self.user.nickname), False)
            info('{} has quit.'.format(self.user.nickname))
            self.server.remove_user(self.user)
        except utils.ClientError as e:
            warning(e.args[0])
        except socket.error:
            pass
        super().finish()

    def send(self, msg_type, **kwargs):
        utils.send_msg(self.wfile, msg_type, **kwargs)

    def send_text(self, text, error=False):
        msg_type = 'error' if error else 'text'
        self.send(msg_type, text=text)

    def send_ok(self):
        self.send('ok')

    def recv(self):
        return utils.recv_msg(self.rfile)

    def broadcast(self, msg_type, obj, include_this_user=True):
        """Send a message to every connected user, possibly exempting the user who's the cause of the message."""

        # todo: change this usage of ``self.server.users`` into thread-safe.
        for user, f_out in self.server.users.items():
            if user == self.user and not include_this_user:
                continue
            utils.send_msg(f_out, msg_type, **obj)

    def broadcast_text(self, text, include_this_user=True):
        self.broadcast('text', {'text': text}, include_this_user)


def start_server(address):
    server = LanServer(address, LanHandler)
    server.serve_forever()
