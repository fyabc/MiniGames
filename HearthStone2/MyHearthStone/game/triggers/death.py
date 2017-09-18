#! /usr/bin/python
# -*- coding: utf-8 -*-

from ..card import Minion, Weapon
from ..events import standard
from ..hero import Hero
from .trigger import StandardBeforeTrigger

__author__ = 'fyabc'


class StdDeathPhase(StandardBeforeTrigger):
    """Standard trigger of death phase."""

    respond = [standard.DeathPhase]

    def process(self, event: respond[0]):
        result = []
        for death in event.deaths:
            if isinstance(death, Hero):
                result.append(standard.HeroDeath(self.game, death))
            elif isinstance(death, Minion):
                result.append(standard.MinionDeath(self.game, death))
            elif isinstance(death, Weapon):
                result.append(standard.WeaponDeath(self.game, death))
        return result
