#! /usr/bin/python
# -*- coding: utf-8 -*-

"""Real time events.

These events will happen and select target(s) real time.
These events contain random target events (may also contain AOE events).

The implementation of these targets must select target when it happens,
not the time it was added into the event engine.

Example:
    1. Spell: Take 1 damage to a random friend minion.
        If I have a "紫罗兰教师", this spell will summon a new minion.
        Then the new minion can be selected as the target.
    2. Spell: Take 1 damage to a random minion.
        If I have a minion "When I play a spell, destroy a random minion",
        I must select the minion after the destroy event.
    3. Spell: Take 4 damage to all minions, THEN take 4 damage to all minions.
        Targets of the second 4 damage cannot be decided at the time of the first 4 damage,
        so I must have a real time event.

Note:
    Is AOEEvent really needed? When an AOE spell is running its `play` method,
    it seems that its targets will not change.
"""

from random import sample

from .base import GameEvent
from .health import Damage, SpellDamage
from ..constants.card import Type_spell
from ..utils.debug import verbose

__author__ = 'fyabc'


class RealTimeEvent(GameEvent):
    def __init__(self, game, where):
        super().__init__(game)
        self.where = where

    def _get_targets(self):
        raise NotImplementedError()

    def _happen(self):
        targets = self._get_targets()

        if targets is None:
            # If not have enough targets, skip and disable it.
            self.disable()
            return

        self._apply_to_targets(targets)

        self._message()

    def _apply_to_targets(self, targets):
        pass


class RandomTargetEvent(RealTimeEvent):
    def __init__(self, game, where, target_number=1):
        super().__init__(game, where)
        self.target_number = target_number

    def _get_targets(self):
        candidates = self.where()

        if not hasattr(candidates, '__len__'):
            candidates = list(candidates)

        if len(candidates) < self.target_number:
            return None

        return sample(candidates, self.target_number)


class RandomTargetDamage(RandomTargetEvent):
    def __init__(self, game, source, value, where, target_number=1):
        super().__init__(game, where, target_number)
        self.source = source
        self.value = value

    def _apply_to_targets(self, targets):
        if self.source.type == Type_spell:
            damage_type = Damage
        else:
            damage_type = SpellDamage

        for target in targets:
            self.game.add_event_quick(damage_type, self.source, target, self.value)

    def __str__(self):
        return '{}({}=>random, value={})'.format(super().__str__(), self.source, self.value)

    def _message(self):
        verbose('{} take {} damage to random target!'.format(self.source, self.value))


__all__ = [
    'RandomTargetEvent',
    'RandomTargetDamage',
]
