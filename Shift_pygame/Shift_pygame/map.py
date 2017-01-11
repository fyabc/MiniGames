#! /usr/bin/python
# -*- encoding: utf-8 -*-

from collections import defaultdict

from .support.vector import Vector2

__author__ = 'fyabc'


class Map:
    ValueBlack = False
    ValueWhite = True

    def __init__(self, array):
        self.matrix = None
        self.elements = defaultdict(list)

    def __getitem__(self, item):
        if isinstance(item, (list, tuple)):
            pass
        elif isinstance(item, Vector2):
            pass
        else:
            raise TypeError('Unsupported index type {}'.format(type(item).__name__))

    def add_element(self, command, *args):
        self.ElementTable[command](self, *args)

    def add_door(self, *args):
        pass

    def add_trap(self, *args):
        pass

    def add_arrow(self, *args):
        pass

    def add_key(self, *args):
        pass

    def add_block(self, *args):
        pass

    def add_lamp(self, *args):
        pass

    def add_mosaic(self, *args):
        pass

    def add_text(self, *args):
        pass

    ElementTable = {
        'D': add_door,
        'T': add_trap,
        'A': add_arrow,
        'K': add_key,
        'B': add_block,
        'L': add_lamp,
        'M': add_mosaic,
        'Text': add_text,
    }
