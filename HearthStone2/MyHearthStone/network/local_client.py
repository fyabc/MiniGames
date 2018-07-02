#! /usr/bin/python
# -*- coding: utf-8 -*-

import socket

from .utils import *
from ..utils.message import entity_message, info

__author__ = 'fyabc'


class BaseLocalClient:
    def __init__(self, user, server_address, **kwargs):
        self.user = user
        self.server_address = server_address
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(server_address)
        self.rfile = self.socket.makefile('rb', 0)
        self.wfile = self.socket.makefile('wb', 0)

        # TODO: Load other information, such as mode, deck, etc.
        info('Create LAN client {}'.format(self))

    def __repr__(self):
        return entity_message(self, {'user': self.user, 'server_address': self.server_address})

    def run(self):
        try:
            self.send(MsgTypes.Text, a=1, b=2)
            self.send_ok()
            self.send_text('Hello from {}'.format(self))
            self.wfile.flush()
        except ConnectionError:
            return

    def send(self, msg_type, **kwargs):
        send_msg(self.wfile, msg_type, **kwargs)

    def recv(self):
        return recv_msg(self.rfile)

    def send_text(self, text, error=False):
        msg_type = MsgTypes.Error if error else MsgTypes.Text
        self.send(msg_type, text=text)

    def send_ok(self):
        self.send(MsgTypes.OK)


class LocalClientV1(BaseLocalClient):
    pass


class LocalClientV2(BaseLocalClient):
    pass


def start_client(version, address, user, **kwargs):
    if version == 1:
        client = LocalClientV1(user, address, **kwargs)
    elif version == 2:
        client = LocalClientV2(user, address, **kwargs)
    else:
        raise ValueError('Unknown version {!r}'.format(version))
    info('Start LAN client {}'.format(client))
    client.run()


__all__ = [
    'BaseLocalClient',
    'LocalClientV1',
    'LocalClientV2',
    'start_client',
]
