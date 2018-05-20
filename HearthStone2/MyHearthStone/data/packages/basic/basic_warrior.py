#! /usr/bin/python
# -*- coding: utf-8 -*-

from MyHearthStone import ext
from MyHearthStone.ext import Minion, Spell, Hero, HeroPower

__author__ = 'fyabc'


###############
# Warrior (9) #
###############


# Warrior (8)
class Warrior(Hero):
    data = {
        'id': 8,
        'klass': 9, 'hero_power': 8,
    }


class 全副武装(HeroPower):
    data = {
        'id': 8,
        'klass': 9, 'is_basic': True, 'cost': 2,
        'have_target': False,
    }

    def run(self, target, **kwargs):
        # TODO
        return []


# 战歌指挥官 (90000)

# 库卡隆精英卫士 (90001)
ext.blank_minion({
    'id': 90001,
    'klass': 9, 'cost': 4, 'attack': 4, 'health': 3,
    'charge': True,
})

# 旋风斩 (90002)

# 冲锋 (90003)

# 顺劈斩 (90004)

# 斩杀 (90005)

# 英勇打击 (90006)

# 盾牌格挡 (90007)

# 炽炎战斧 (90008)
ext.blank_weapon({
    'id': 90008,
    'type': 2, 'klass': 9, 'cost': 3, 'attack': 3, 'health': 2,
})

# 奥金斧 (90009)
