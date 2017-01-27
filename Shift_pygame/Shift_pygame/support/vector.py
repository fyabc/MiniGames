#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'fyabc'


class Vector2:
    """A simple 2-D vector."""

    __slots__ = ('x', 'y')

    origin = None

    def __init__(self, *args):
        if len(args) == 2:
            self.x, self.y = args
        elif len(args) == 1:
            self.x, self.y = args[0]
        else:
            raise TypeError('unexpected type of Vector2 initializer')

    def __iter__(self):
        yield self.x
        yield self.y

    def __getitem__(self, item):
        if item == 0:
            return self.x
        elif item == 1:
            return self.y
        else:
            raise IndexError('index out of range')

    def __setitem__(self, key, value):
        if key == 0:
            self.x = value
        elif key == 1:
            self.y = value
        else:
            raise IndexError('index out of range')

    def __add__(self, other):
        _x, _y = other
        return Vector2(self.x + _x, self.y + _y)

    def __iadd__(self, other):
        _x, _y = other
        self.x += _x
        self.y += _y

    def __sub__(self, other):
        _x, _y = other
        return Vector2(self.x - _x, self.y - _y)

Vector2.origin = Vector2(0., 0.)
