#! /usr/bin/python
# -*- coding: utf-8 -*-

from .game_event import GameEvent
from .death_events import MinionDeath
from ..utils import verbose

__author__ = 'fyabc'


class Damage(GameEvent):
    def __init__(self, game, source, target, value):
        super(Damage, self).__init__(game)
        self.source = source
        self.target = target
        self.value = value

    def __str__(self):
        return '{}({}=>{}, value={})'.format(super().__str__(), self.source, self.target, self.value)

    def _happen(self):
        self._message()

        died = self.target.take_damage(self.source, self.value, self)

        if died:
            verbose('{} kill {}!'.format(self.source, self.target))
            # todo: add `MinionDeath` event
            if self.target in self.game.players:
                # Target is hero: pass
                pass
            else:
                # Target is minion: minion death
                self.game.add_event_quick(MinionDeath, self.target)

    def _message(self):
        verbose('{} take {} damage to {}!'.format(self.source, self.value, self.target))


__all__ = [
    'Damage',
]
