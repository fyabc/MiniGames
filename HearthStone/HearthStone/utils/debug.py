#! /usr/bin/python
# -*- coding: utf-8 -*-

from sys import platform
from functools import partial
from contextlib import contextmanager

__author__ = 'fyabc'

WIN32 = platform == 'win32'


if WIN32:
    from ctypes import windll
    import win32api
    import win32console

    ConsoleColors = {
        'BlackB': None,
        'WhiteF': None,
    }

else:
    ConsoleColors = {
        'BlackB': None,
        'WhiteF': None,
    }


_color_status = [
    ConsoleColors['WhiteF'],
    ConsoleColors['BlackB'],
]


def set_color(fg=ConsoleColors['WhiteF'], bg=ConsoleColors['BlackB']):
    _color_status[0] = fg
    _color_status[1] = bg


def color_msg(msg, fg=ConsoleColors['WhiteF'], bg=ConsoleColors['BlackB'], **kwargs):
    old_color = _color_status[:]
    set_color(fg, bg)
    print(msg, **kwargs)
    set_color(*old_color)


# Debug levels.
LEVEL_DEBUG = 0
LEVEL_VERBOSE = 1
LEVEL_INFO = 2
LEVEL_COMMON = 2.5
LEVEL_WARNING = 3
LEVEL_ERROR = 4


_debug_level = LEVEL_COMMON


def set_debug_level(new_level):
    global _debug_level
    _debug_level = new_level


def get_debug_level():
    return _debug_level


def message(*args, **kwargs):
    level = kwargs.pop('level', LEVEL_INFO)
    if level >= _debug_level:
        print(*args, **kwargs)


debug = partial(message, level=LEVEL_DEBUG)
verbose = partial(message, level=LEVEL_VERBOSE)
info = partial(message, level=LEVEL_INFO)
warning = partial(message, level=LEVEL_WARNING)
error = partial(message, level=LEVEL_ERROR)


@contextmanager
def msg_block(msg, level=LEVEL_INFO):
    message('{}... '.format(msg), end='', level=level)
    yield
    message('Done', level=level)

__all__ = [
    'ConsoleColors',
    'set_color',
    'color_msg',
    'get_debug_level',
    'set_debug_level',
    'LEVEL_DEBUG',
    'LEVEL_VERBOSE',
    'LEVEL_INFO',
    'LEVEL_COMMON',
    'LEVEL_WARNING',
    'LEVEL_ERROR',
    'message',
    'debug',
    'verbose',
    'info',
    'warning',
    'error',
    'msg_block',
]
