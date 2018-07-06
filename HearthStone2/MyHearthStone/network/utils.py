#! /usr/bin/python
# -*- coding: utf-8 -*-

"""Utilities of network.

Message format:
Compressed JSON string
{
    "type": "text",
    # Other information ...
}
"""

import json

from ..utils.error import GameError

__author__ = 'fyabc'


# Exceptions.

class NetworkError(GameError):
    pass


class ServerFull(GameError):
    def __init__(self, server):
        super().__init__('Server(address={}) already full!'.format(server.server_address))
        self.server = server


class UserAlreadyExists(GameError):
    def __init__(self, server, user):
        super().__init__('{} already exists in Server(address={})!'.format(user, server))
        self.user = user
        self.server = server


class UserNotExists(GameError):
    def __init__(self, server, user):
        super().__init__('{} does not exist in Server(address={})!'.format(user, server))
        self.user = user
        self.server = server


class MasterAlreadyExists(GameError):
    def __init__(self, server, user):
        super().__init__('Master {} already exists in Server(address={})!'.format(user, server))
        self.user = user
        self.server = server


# Message utilities.

def send_dict(fd, d):
    fd.write(((json.dumps(d, separators=(',', ':')) + '\n').encode()))


def recv_dict(fd):
    s = fd.readline().strip().decode()
    if not s:
        return None
    return json.loads(s)


class MsgTypes:
    Text = 'text'
    OK = 'ok'
    Error = 'error'

    Default = Text


def send_msg(fd, msg_type, **kwargs):
    kwargs['type'] = msg_type
    send_dict(fd, kwargs)


def recv_msg(fd):
    """Receive message.

    :param fd:
    :return: Pair of (msg_type, msg_dict)
        If no data received, return (None, None), it usually means connection closed.
    :rtype: tuple
    """
    d = recv_dict(fd)
    if d is None:
        return None, None
    return d.get('type', MsgTypes.Default), d


class UserState:
    Invalid = -1
    WaitUserData = 0
    CloseConnection = 10


__all__ = [
    'NetworkError',
    'ServerFull',
    'UserAlreadyExists',
    'UserNotExists',
    'MasterAlreadyExists',

    'MsgTypes',
    'send_dict', 'recv_dict',
    'send_msg', 'recv_msg',

    'UserState',
]
