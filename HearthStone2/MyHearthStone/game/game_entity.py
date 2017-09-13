#! /usr/bin/python
# -*- coding: utf-8 -*-

from collections import ChainMap

from ..utils.constants import C

__author__ = 'fyabc'


class GameEntity:
    """The base class of all game entities."""

    def __init__(self, game):
        self.game = game

        # oop(Order Of Play).
        # All game entities have this attribute, and share the same oop list.
        self.oop = None


class SetDataMeta(type):
    """This metaclass is used for setting `data` attribute of cards automatically.

    This metaclass will set the `data` attribute with a new `ChainMap` instance
    (if its first base class does not have `data` attribute) or the `data` attribute
    of its first base class (if it has `data` attribute).
    The value of new child of `data` is stored in `_data` attribute of the class.
    """

    @staticmethod
    def __new__(mcs, name, bases, ns):
        # This called before the class created.
        # print('New:', mcs, name, bases, ns)

        # assert len(bases) == 1, 'This metaclass requires the class have exactly 1 superclass.'

        base_data = getattr(bases[0], 'data', ChainMap()) if bases else ChainMap()
        ns['data'] = base_data.new_child(ns.get('_data', {}))

        if C.Game.DocDescription:
            doc = ns.get('__doc__', None)
            if doc is not None and not doc.startswith('[NO_DESCRIPTION]'):
                ns['data']['description'] = doc

        return type.__new__(mcs, name, bases, ns)

    def __init__(cls, name, bases, ns):
        # This called after the class created.
        # print('Init:', cls, name, bases, ns)

        super().__init__(name, bases, ns)
