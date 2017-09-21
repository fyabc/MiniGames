#! /usr/bin/python
# -*- coding: utf-8 -*-

import socket
import threading

from . import utils
from ..utils.message import message

__author__ = 'fyabc'


class LanClient:
    def __init__(self, user):
        self.user = user
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(self.user.address)
        self.rfile = self.socket.makefile('rb', 0)
        self.wfile = self.socket.makefile('wb', 0)
        self.input_thread = None

        self.start()

        self.run()

    def start(self):
        # 1. Send user data to server.
        self.send('user_data', nickname=self.user.nickname, deck_code=self.user.deck_code)

        self.input_thread = self.InputThread(self.wfile)
        t = threading.Thread(target=self.input_thread.run)
        t.setDaemon(True)
        t.start()

    def run(self):
        running = True
        while running:
            try:
                msg = self.recv()
            except ConnectionError:
                break

            message(msg)

            if msg['type'] == 'terminated':
                running = False
        self.input_thread.done = True

    def send(self, msg_type, **kwargs):
        utils.send_msg(self.wfile, msg_type, **kwargs)

    def send_text(self, text, error=False):
        msg_type = 'error' if error else 'text'
        self.send(msg_type, text=text)

    def send_ok(self):
        self.send('ok')

    def recv(self):
        return utils.recv_msg(self.rfile)

    class InputThread:
        def __init__(self, wfile):
            self.wfile = wfile
            self.done = False

        def run(self):
            """Echo standard input to the chat server until told to stop."""

            # todo: add input method
            while not self.done:
                pass


def start_client(address, nickname, deck_code):
    LanClient(utils.User(address, nickname, deck_code))
