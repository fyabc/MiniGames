#! /usr/bin/python
# -*- coding: utf-8 -*-

from .game_event import GameEvent
from ..utils import verbose

__author__ = 'fyabc'


class Damage(GameEvent):
    def __init__(self, game, source, target, value):
        super(Damage, self).__init__(game)
        self.source = source
        self.target = target
        self.value = value

    def _happen(self):
        self._message()

        # todo: move add event code into handlers.
        died = self.target.take_damage(self.source, self.value)

        if died:
            verbose('{} kill {}!'.format(self.source, self.target))
            # todo: add `MinionDeath` event

    def _message(self):
        verbose('{} take {} damage to {}!'.format(self.source, self.value, self.target))


__all__ = [
    'Damage',
]
