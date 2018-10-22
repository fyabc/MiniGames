#! /usr/bin/python
# -*- coding: utf-8 -*-

from cocos import director

__author__ = 'fyabc'


_Width, _Height = None, None


def get_width():
    global _Width, _Height
    if _Width is None:
        _Width, _Height = director.director.get_window_size()
    return _Width


def get_height():
    global _Width, _Height
    if _Height is None:
        _Width, _Height = director.director.get_window_size()
    return _Height


def pos(x, y, base=None, scale=1.0):
    if base is not None:
        return base[0] * x * scale, base[1] * y * scale
    global _Width, _Height
    if _Width is None:
        _Width, _Height = director.director.get_window_size()
    return _Width * x * scale, _Height * y * scale


def pos_x(x, base=None, scale=1.0):
    return pos(x, 0.0, base, scale)[0]


def pos_y(y, base=None, scale=1.0):
    return pos(0.0, y, base, scale)[1]
