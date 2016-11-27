#! /usr/bin/python
# -*- coding: utf-8 -*-

from sys import platform


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
