#! /usr/bin/python
# -*- coding: utf-8 -*-

"""Classic package."""

from MyHearthStone.ext import Spell
from MyHearthStone.ext import std_events

__author__ = 'fyabc'

PackageID = 1


###############
# Neutral (0) #
###############


############
# Mage (3) #
############

# 冰枪术(1030002) -> 荣誉室

class 炎爆术(Spell):
    _data = {
        'id': 1030013, 'package': PackageID,
        'type': 1, 'rarity': 3, 'klass': 3, 'CAH': [10],
        'have_target': True,
    }

    def run(self, target):
        return [std_events.damage_events(self.game, self, target, 10)]
