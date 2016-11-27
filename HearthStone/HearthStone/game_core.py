#! /usr/bin/python
# -*- coding: utf-8 -*-

from HearthStone.event_framework import EventEngine


__author__ = 'fyabc'


class Hero:
    pass


class Game:
    """The class of the game.

    This class contains:
        an EventEngine
        some game data
            minions
            cards
            heroes
            ...
    """

    def __init__(self):
        self.engine = EventEngine()
