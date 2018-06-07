#! /usr/bin/python
# -*- coding: utf-8 -*-

from MyHearthStone import ext
from MyHearthStone.ext import Spell, Minion
from MyHearthStone.ext import std_events, std_triggers
from MyHearthStone.utils.game import Race, Zone

__author__ = 'fyabc'


############
# Mage (3) #
############

# 烈焰巨兽 (11030007)
class 烈焰巨兽(Minion):
    """[NOTE]: This is a classic card of on-draw effect."""
    data = {
        'id': 11030007,
        'rarity': 4, 'klass': 3, 'cost': 7, 'attack': 7, 'health': 7,
        'race': [Race.Mech],
    }

    class Trig_烈焰巨兽(std_triggers.Trigger):
        respond = [std_events.GenericDrawCard]
        zones = [Zone.Hand]

        def process(self, event: respond[0]):
            if event.card is not self.owner:
                return []
            targets = ext.collect_all(self, except_self=False, oop=True)
            return [std_events.AreaDamage(self.game, self.owner, targets, [2 for _ in targets])]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Trig_烈焰巨兽(self.game, self)
