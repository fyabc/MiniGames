#! /usr/bin/python
# -*- coding: utf-8 -*-

"""Damage events.

See <https://hearthstone.gamepedia.com/Advanced_rulebook#Damage_and_Healing> for details.
"""

import random

from .event import Event, DelayResolvedEvent, AreaEvent
from .misc import LoseDivineShield, LoseStealth
from ...utils.constants import version_larger_equal
from ...utils.game import DHBonusEventType

__author__ = 'fyabc'


class Damage(DelayResolvedEvent):
    def __init__(self, game, owner, target, value, work_done=False, apply_dh_bonus=True):
        super().__init__(game, owner, work_done=work_done)
        self.target = target
        self.value = value
        self.apply_dh_bonus = apply_dh_bonus

    def _repr(self):
        return super()._repr(source=self.owner, target=self.target, value=self.value)

    def do_real_work(self):
        """Do the real work of damage event.

        See <https://hearthstone.gamepedia.com/Damage#Advanced_rules> for more details.
        """
        self.pending_events = []

        # Apply proposed damage bonuses (unless it is from a distributed damage event).
        if self.apply_dh_bonus:
            self.value = self.owner.get_proposed_dh_value(self.value, DHBonusEventType.Damage)

        if self.value <= 0:
            self.disable()
            return

        if self.target.divine_shield:
            self.target.divine_shield = False
            self.value = 0
            self.disable()
            self.pending_events.append(LoseDivineShield(self.game, self.target))
            return

        # todo: need test and add more
        self.target.take_damage(self.value)

        # Lose stealth (before patch 11.0.0).
        if not version_larger_equal("11.0.0"):
            if self.owner.stealth:
                self.owner.stealth = False
                self.pending_events.append(LoseStealth(self.game, self.owner))


class AreaDamage(AreaEvent):
    """The area of effect (AoE) damage event.

    See docstring of ``MyHearthStone.game.events.healing.AreaHealing`` for more details.
    """

    def __init__(self, game, owner, targets, values):
        super().__init__(game, owner, events=[
            Damage(game, owner, target, value, work_done=True)
            for target, value in zip(targets, values)])


class RandomDamage(Damage):
    def __init__(self, game, owner, collect_fn, value, apply_dh_bonus=True, random_fn=None):
        super().__init__(game, owner, None, value, work_done=False, apply_dh_bonus=apply_dh_bonus)
        self.collect_fn = collect_fn

        # By default, choose one in equal probability.
        self.random_fn = random.choice if random_fn is None else random_fn

    def do_real_work(self):
        # [NOTE]: Collect when running this event (previous events have been resolved)
        if self.target is None:
            candidates = self.collect_fn()

            # If no available target, just stop and disable it.
            if not candidates:
                self.disable()
                return

            self.target = self.random_fn(candidates)
        super().do_real_work()


class DistributedDamage(Event):
    def __init__(self, game, owner, value, collect_fn, random_fn=None):
        super().__init__(game, owner)
        self.value = value
        self.collect_fn = collect_fn
        self.random_fn = random_fn

    def do(self):
        self.value = self.owner.get_proposed_dh_value(self.value, DHBonusEventType.Damage)

        if self.value <= 0:
            self.disable()
            return []

        return [
            RandomDamage(self.game, self.owner, self.collect_fn, 1, apply_dh_bonus=False, random_fn=self.random_fn)
            for _ in range(self.value)
        ]


__all__ = [
    'Damage',
    'AreaDamage',
    'RandomDamage',
    'DistributedDamage',
]
