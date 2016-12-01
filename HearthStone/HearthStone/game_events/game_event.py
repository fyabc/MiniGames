#! /usr/bin/python
# -*- coding: utf-8 -*-

from ..event_framework import Event
from ..utils import verbose

__author__ = 'fyabc'


class GameEvent(Event):
    def __init__(self, game):
        super(GameEvent, self).__init__()
        self.game = game

    def _happen(self):
        verbose('{} happen!'.format(self))


__all__ = [
    'GameEvent',
]
