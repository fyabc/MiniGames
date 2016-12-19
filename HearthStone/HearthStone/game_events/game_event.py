#! /usr/bin/python
# -*- coding: utf-8 -*-

"""The base class of all game events."""

# [NOTE] It seems that (not sure):
#   1. When a event create another event, the new event should be prepend to the head of the event queue.
#   2. When another thing (handler, battle_cry) create another event,
#   the new event should be appended to the tail of the event queue.

from ..event_framework import Event
from ..utils.debug_utils import verbose

__author__ = 'fyabc'


class GameEvent(Event):
    def __init__(self, game):
        super(GameEvent, self).__init__()
        self.game = game

    def _happen(self):
        self._message()

    def _message(self):
        verbose('{} happen!'.format(self))


__all__ = [
    'GameEvent',
]
