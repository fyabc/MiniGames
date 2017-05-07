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
from .damage import Damage, SpellDamage
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
    def __init__(self, game, source, value, where, target_number=1, damage_type=None):
        super().__init__(game, where, target_number)
        self.source = source
        self.value = value
        if damage_type is None:
            if self.source.type == Type_spell:
                self.damage_type = SpellDamage
            else:
                self.damage_type = Damage
        else:
            self.damage_type = damage_type

    def _apply_to_targets(self, targets):
        for target in targets:
            self.game.insert_event_quick(self.damage_type, self.source, target, self.value)

    def __str__(self):
        return '{}({}=>random, value={})'.format(super().__str__(), self.source, self.value)

    def _message(self):
        verbose('{} take {} damage to random target!'.format(self.source, self.value))


class ArcaneMissilesDamage(GameEvent):
    """This is special spell damage of 'Arcane Missiles' and 'Avenging Wrath'.

    The effect of Spell Power on it is different from common spell damage.
    
    [NOTE] This is NOT a subclass of Damage or SpellDamage!
    """

    def __init__(self, game, spell, value):
        super().__init__(game)
        self.source = spell
        self.value = value

    def __str__(self):
        return '{}({}=>random, value={})'.format(super().__str__(), self.source, self.value)

    @property
    def spell(self):
        return self.source

    def _happen(self):
        for _ in range(self.value):
            self.game.add_event_quick(RandomTargetDamage, self.source, 1,
                                      self.game.range(1 - self.source.player_id, exclude_dead=True),
                                      damage_type=Damage)

        self._message()

    def _message(self):
        verbose('{} take Arcane Missiles Damage of value {}!'.format(self.source, self.value))


__all__ = [
    'RandomTargetEvent',
    'RandomTargetDamage',
    'ArcaneMissilesDamage',
]
