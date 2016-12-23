#! /usr/bin/python
# -*- coding: utf-8 -*-

"""Real time events.

These events will happen and select target(s) real time.
These events contains random target events and AOE events.

The implementation of these targets must select target when it happens,
not the time it was added into the event engine.

Example:
    1. Spell: Take 1 damage to a random friend minion.
        If I have a "紫罗兰教师", this spell will summon a new minion.
        Then the new minion can be selected as the target.
    2. Spell: Take
"""

from random import sample

from .game_event import GameEvent
from .health_events import Damage, SpellDamage
from ..constants.card_constants import Type_spell
from ..utils.debug_utils import verbose

__author__ = 'fyabc'


class RealTimeEvent(GameEvent):
    def __init__(self, game, where):
        super().__init__(game)
        self.where = where

    def _get_targets(self):
        raise NotImplementedError()


class RandomTargetEvent(RealTimeEvent):
    def __init__(self, game, where, target_number=1):
        super().__init__(game, where)
        self.target_number = target_number

    def _get_targets(self):
        candidates = self.where()

        if len(candidates) < self.target_number:
            return None

        return sample(candidates, self.target_number)


class AOEEvent(RealTimeEvent):
    def _get_targets(self):
        return self.where()


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
