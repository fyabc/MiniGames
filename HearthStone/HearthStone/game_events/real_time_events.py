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
    2. Spell(烈焰风暴): Take 4 damage to all enemy minions.
        If enemy has a "颤地者特罗格佐尔", it will summon a new minion.
        Then the new minion will be selected as the target.
    3. Spell: Take 1 damage to a random minion.
        If I have a minion "When I play a spell, destroy a random minion",
        I must select the minion after the destroy event.

Note:
    Is AOEEvent really needed? When an AOE spell is running its `play` method,
    it seems that its targets will not change.
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

        if len(candidates) < self.target_number:
            return None

        return sample(candidates, self.target_number)


class AOEEvent(RealTimeEvent):
    def _get_targets(self):
        candidates = self.where()

        if not candidates:
            return None
        return candidates


def _apply_damage(self, targets):
    if self.source.type == Type_spell:
        damage_type = Damage
    else:
        damage_type = SpellDamage

    for target in targets:
        self.game.add_event_quick(damage_type, self.source, target, self.value)


class RandomTargetDamage(RandomTargetEvent):
    def __init__(self, game, source, value, where, target_number=1):
        super().__init__(game, where, target_number)
        self.source = source
        self.value = value

    _apply_to_targets = _apply_damage

    def __str__(self):
        return '{}({}=>random, value={})'.format(super().__str__(), self.source, self.value)

    def _message(self):
        verbose('{} take {} damage to random target!'.format(self.source, self.value))


class AOEDamage(AOEEvent):
    def __init__(self, game, source, value, where):
        super().__init__(game, where)
        self.source = source
        self.value = value

    _apply_to_targets = _apply_damage

    def __str__(self):
        return '{}({}=>AOE, value={})'.format(super().__str__(), self.source, self.value)

    def _message(self):
        verbose('{} take {} damage to all matched targets!'.format(self.source, self.value))


__all__ = [
    'RandomTargetEvent',
    'AOEEvent',
    'RandomTargetDamage',
    'AOEDamage',
]
