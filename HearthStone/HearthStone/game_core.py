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
            turns
            minions
            cards
            heroes
            (history manager)
            ...
    """

    def __init__(self):
        # Event engine.
        self.engine = EventEngine()

        # Game data.

    def create_event(self, event_type, *args, **kwargs):
        return event_type(self, *args, **kwargs)

    def create_handler(self, handler_type, *args, **kwargs):
        return handler_type(self, *args, **kwargs)
