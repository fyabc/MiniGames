#! /usr/bin/python
# -*- coding: utf-8 -*-

"""Standard damage triggers.

See <https://hearthstone.gamepedia.com/Advanced_rulebook#Damage_and_Healing> for details.
"""

from ..events import standard
from .trigger import StandardBeforeTrigger

__author__ = 'fyabc'


class StdPreDamage(StandardBeforeTrigger):
    """Standard trigger of pre-damage."""

    respond = [standard.PreDamage]

    def process(self, event: respond[0]):
        damage = event.damage
        if damage.value <= 0:
            # [NOTE] May need to remain this event here?
            event.disable()
            damage.disable()
            return []

        if damage.target.divine_shield:
            damage.target.divine_shield = False
            damage.value = 0
            event.disable()
            damage.disable()
            return [standard.LoseDivineShield(self.game, damage.target)]

        return []


class StdDamage(StandardBeforeTrigger):
    """Standard trigger of damage."""

    respond = [standard.Damage]

    def process(self, event: respond[0]):
        # todo: need test and add more
        event.target.take_damage(event.value)

        return []
