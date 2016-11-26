#! /usr/bin/python
# -*- coding: utf-8 -*-

from HearthStone.event_framework import Event, Handler, EventEngine


__author__ = 'fyabc'


class GameEvent(Event):
    def __init__(self, game):
        super(GameEvent, self).__init__()
        self.game = game


class GameHandler(Handler):
    def __init__(self, game):
        super(GameHandler, self).__init__()
        self.game = game


class Game:
    """The class of the game.

    This class contains:
        an EventEngine
        some game data
            minions
            cards
            hero
            ...
    """

    def __init__(self):
        self.engine = EventEngine()
