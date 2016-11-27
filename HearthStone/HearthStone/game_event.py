#! /usr/bin/python
# -*- coding: utf-8 -*-
from HearthStone.event_framework import Event

__author__ = 'fyabc'


class GameEvent(Event):
    def __init__(self, game):
        super(GameEvent, self).__init__()
        self.game = game

    def happen(self):
        print('{} happen!'.format(self))


class TurnBegin(GameEvent):
    def __init__(self, game):
        super(TurnBegin, self).__init__(game)


__all__ = [
    'GameEvent',
    'TurnBegin',
]
