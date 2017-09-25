#! /usr/bin/python
# -*- coding: utf-8 -*-

import json

__author__ = 'fyabc'


def _ensure_newline(s):
    if s and s[-1] != '\n':
        s += '\r\n'
    return s


def send_obj(fd, obj):
    fd.write((json.dumps(obj, separators=(',', ':')) + '\n').encode())


def recv_obj(fd):
    return json.loads(fd.readline().strip().decode())


# Message are dicts (in JSON format)
DefaultMsgType = 'text'


def send_msg(fd, msg_type, **kwargs):
    # Default message type
    kwargs['type'] = msg_type
    send_obj(fd, kwargs)


recv_msg = recv_obj


class ClientError(Exception):
    """The exception class for client errors."""

    pass


class NetworkUser:
    """The network user class."""

    def __init__(self, address, nickname, deck_code):
        self.address = address
        self.nickname = nickname
        self.deck_code = deck_code
        self.player_id = None

    def __eq__(self, other):
        return (self.address, self.nickname) == (other.address, other.nickname)

    def __hash__(self):
        return hash((self.address, self.nickname))


MessageTypes = {
    'text',
    'error',
    'ok',
    'user_data',
    'game_status',
}
