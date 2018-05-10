#! /usr/bin/python
# -*- coding: utf-8 -*-

"""Classic package."""

from MyHearthStone import ext
from MyHearthStone.ext import blank_minion
from MyHearthStone.ext import Minion, Spell, Weapon
from MyHearthStone.ext import std_events
from MyHearthStone.utils.game import Race

__author__ = 'fyabc'

PackageID = 1


###############
# Neutral (0) #
###############

# 小精灵
blank_minion({
    'id': 1000000,
    'rarity': 1, 'cost': 0, 'attack': 1, 'health': 1,
})

# 持盾卫士
blank_minion({
    'id': 1000001,
    'rarity': 1, 'cost': 1, 'attack': 0, 'health': 4,
    'taunt': True,
})

# 银色侍从
blank_minion({
    'id': 1000003,
    'rarity': 1, 'cost': 1, 'attack': 1, 'health': 1,
    'divine_shield': True,
})

# 幼龙鹰
blank_minion({
    'id': 1000005,
    'rarity': 1, 'cost': 1, 'attack': 1, 'health': 1,
    'windfury': True, 'race': [Race.Beast],
})


class 战利品贮藏者(Minion):
    data = {
        'id': 1000008,
        'rarity': 1, 'cost': 2, 'attack': 2, 'health': 1,
    }

    def run_deathrattle(self):
        return [std_events.DrawCard(self.game, self, self.player_id)]


############
# Mage (3) #
############

# 冰枪术(1030002) -> 荣誉室

class 炎爆术(Spell):
    data = {
        'id': 1030013,
        'type': 1, 'rarity': 3, 'klass': 3, 'cost': 10,
        'have_target': True,
    }

    run = ext.damage_fn(10)


class 大法师安东尼达斯(Minion):
    data = {
        'id': 1030014,
        'rarity': 4, 'klass': 3, 'cost': 7, 'attack': 5, 'health': 7,
    }


###############
# Warrior (8) #
###############


class 血吼(Weapon):
    data = {
        'id': 1080013,
        'type': 2, 'rarity': 3, 'klass': 8, 'cost': 7, 'attack': 7, 'health': 1,
    }
