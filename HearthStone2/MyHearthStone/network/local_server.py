#! /usr/bin/python
# -*- coding: utf-8 -*-

"""The LAN server of HearthStone."""

# TODO: Two designs:
#   1. Fat-client:
#       Each client (user) maintain a game instance, broadcast player actions between them.
#   2. Fat-server:
#       Only the server maintain a game instance, broadcast its status between them.

import socketserver
import threading

from .utils import *
from ..utils.constants import C
from ..utils.message import warning, info, entity_message

__author__ = 'fyabc'


class UserState:
    Invalid = -1
    WaitUserData = 0
    CloseConnection = 10


class BaseLocalServer(socketserver.ThreadingTCPServer):
    def __init__(self, server_address, RequestHandlerClass, bind_and_activate=True, **kwargs):
        super().__init__(server_address, RequestHandlerClass, bind_and_activate=bind_and_activate)

        SMC = C.LAN.ServerMaxCapacity
        capacity = kwargs.pop('capacity', SMC)
        if capacity > SMC:
            warning('LAN server capacity must <= {}, change given capacity {} to {}'.format(SMC, capacity, SMC))
            capacity = SMC
        self.capacity = capacity

        info('Create LAN server {}'.format(self))

    def __repr__(self):
        return entity_message(self, {'address': self.server_address, 'capacity': self.capacity})


class LocalServerV1(BaseLocalServer):
    """The server class (fat-server version)."""


class LocalServerV2(BaseLocalServer):
    """The server class (fat-client version)."""

    def __init__(self, server_address, RequestHandlerClass, bind_and_activate=True, **kwargs):
        super().__init__(server_address, RequestHandlerClass, bind_and_activate=bind_and_activate, **kwargs)

        self.users = {}
        self.master = None
        self.game_users = []

        # Lock for users in the network.
        self._user_lock = threading.Lock()

    def add_user(self, user, output_fd, is_master=False):
        with self._user_lock:
            if len(self.users) >= self.capacity:
                raise ServerFull(self)
            elif user in self.users:
                raise UserAlreadyExists(self, user)
            else:
                if is_master:
                    if self.master is not user:
                        raise MasterAlreadyExists(self, user)
                    else:
                        self.master = user
                self.users[user] = output_fd

    def remove_user(self, user):
        with self._user_lock:
            if user not in self.users:
                raise UserNotExists(self, user)
            else:
                if self.master is user:
                    # TODO: Assign the new master?
                    pass
                del self.users[user]

    def prepare_start_game(self):
        pass

    # TODO: LAN-specific callbacks, send updates to all users.


class BaseLocalHandler(socketserver.StreamRequestHandler):
    def __init__(self, request, client_address, server):
        self.user = None
        self.state = UserState.Invalid

        super().__init__(request, client_address, server)

    def setup(self):
        info('Request from client address {}'.format(self.client_address))
        super().setup()

    def handle(self):
        # TODO
        try:
            while True:
                if self.state == UserState.Invalid:
                    self._handle_init()
                elif self.state == UserState.CloseConnection:
                    self._close_connection()
                    break
                else:
                    pass
            pass
        except ConnectionError as e:
            print('Connection error:', e)

    def _handle_init(self):
        """Ask user data from client, do the initialize."""
        # TODO: Replace this debug impl into real impl.
        msg_type, d = self.recv()
        print('Receive message of type {}'.format(msg_type))
        print('Message value: {}'.format(d))

        if d is None:
            self.state = UserState.CloseConnection

    def _close_connection(self):
        info('Connection to {} closed'.format(self.client_address))

    def finish(self):
        super().finish()

    def send(self, msg_type, **kwargs):
        send_msg(self.wfile, msg_type, **kwargs)

    def recv(self):
        return recv_msg(self.rfile)

    def send_text(self, text, error=False):
        msg_type = MsgTypes.Error if error else MsgTypes.Text
        self.send(msg_type, text=text)

    def send_ok(self):
        self.send(MsgTypes.OK)

    def broadcast(self, msg_type, d):
        pass


class LocalHandlerV1(BaseLocalHandler):
    def __init__(self, request, client_address, server):
        super().__init__(request, client_address, server)

    def setup(self):
        super().setup()

    def finish(self):
        super().finish()


class LocalHandlerV2(BaseLocalHandler):
    def __init__(self, request, client_address, server):
        super().__init__(request, client_address, server)

    def setup(self):
        super().setup()

    def finish(self):
        super().finish()


def start_server(version, address, **kwargs):
    if version == 1:
        server = LocalServerV1(address, LocalHandlerV1, **kwargs)
    elif version == 2:
        server = LocalServerV2(address, LocalHandlerV2, **kwargs)
    else:
        raise ValueError('Unknown version {!r}'.format(version))
    info('Start LAN server {}'.format(server))
    server.serve_forever()


__all__ = [
    'start_server',
]
