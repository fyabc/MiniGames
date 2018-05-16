#! /usr/bin/python
# -*- coding: utf-8 -*-

"""Damage events.

See <https://hearthstone.gamepedia.com/Advanced_rulebook#Damage_and_Healing> for details.
"""

from .event import Phase
from .misc import LoseDivineShield, LoseStealth
from ...utils.constants import version_le

__author__ = 'fyabc'


class PreDamage(Phase):
    def __init__(self, game, damage):
        super().__init__(game, damage.owner)
        self.damage = damage

    def _repr(self):
        return super()._repr(source=self.owner, target=self.damage.target, value=self.damage.value)

    def do(self):
        damage = self.damage
        if damage.value <= 0:
            # [NOTE] May need to remain this event here?
            self.disable()
            damage.disable()
            return []

        if damage.target.divine_shield:
            damage.target.divine_shield = False
            damage.value = 0
            self.disable()
            damage.disable()
            return [LoseDivineShield(self.game, damage.target)]

        return []


class Damage(Phase):
    def __init__(self, game, owner, target, value):
        super().__init__(game, owner)
        self.target = target
        self.value = value

    def _repr(self):
        return super()._repr(source=self.owner, target=self.target, value=self.value)

    def do(self):
        # todo: need test and add more
        self.target.take_damage(self.value)

        result = []

        # Lose stealth (before patch 11.0.0).
        if not version_le("11.0.0"):
            if self.owner.stealth:
                self.owner.stealth = False
                result.append(LoseStealth(self.game, self.owner))

        return result


def damage_events(game, owner, target, value):
    """Utility to get damage event sequences.

    New damage cards can use this API to create damage events.
    """

    damage = Damage(game, owner, target, value)
    return [
        PreDamage(game, damage),
        damage,
    ]
