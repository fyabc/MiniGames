#! /usr/bin/python
# -*- coding: utf-8 -*-

"""Damage events.

See <https://hearthstone.gamepedia.com/Advanced_rulebook#Damage_and_Healing> for details.
"""

from .event import DelayResolvedEvent, AreaEvent
from .misc import LoseDivineShield, LoseStealth
from ...utils.constants import version_larger_equal
from ...utils.game import DHBonusEventType

__author__ = 'fyabc'


class Damage(DelayResolvedEvent):
    def __init__(self, game, owner, target, value, work_done=False):
        super().__init__(game, owner, work_done=work_done)
        self.target = target
        self.value = value

    def _repr(self):
        return super()._repr(source=self.owner, target=self.target, value=self.value)

    def do_real_work(self):
        """Do the real work of damage event.

        See <https://hearthstone.gamepedia.com/Damage#Advanced_rules> for more details.
        """
        self.pending_events = []

        # Apply proposed damage bonuses.
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


__all__ = [
    'Damage',
    'AreaDamage',
]
