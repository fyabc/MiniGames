#! /usr/bin/python
# -*- coding: utf-8 -*-

from random import sample

from .game_event import GameEvent
from .health_events import Damage, SpellDamage
from ..constants.card_constants import Type_spell
from ..utils.debug_utils import verbose

__author__ = 'fyabc'


class RandomTargetDamage(GameEvent):
    """Random target damage.

    The damage will randomly select its target(s) when happening.
    Note:
        Because the target may died or removed from the desk,
        so we cannot select the target when the event is added to event engine.
    """

    def __init__(self, game, source, value, where, target_number=1):
        super().__init__(game)
        self.source = source
        self.value = value
        self.where = where
        self.target_number = target_number

    def _happen(self):
        candidates = self.where()

        if len(candidates) < self.target_number:
            # If not have enough targets, skip and disable it.
            self.disable()
            return

        targets = sample(candidates, self.target_number)

        if self.source.type == Type_spell:
            damage_type = Damage
        else:
            damage_type = SpellDamage

        for target in targets:
            self.game.add_event_quick(damage_type, self.source, target, self.value)

        self._message()

    def __str__(self):
        return '{}({}=>random, value={})'.format(super().__str__(), self.source, self.value)

    def _message(self):
        verbose('{} take {} damage to random target!'.format(self.source, self.value))


__all__ = [
    'RandomTargetDamage',
]
