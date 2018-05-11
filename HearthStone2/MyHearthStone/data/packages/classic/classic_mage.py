#! /usr/bin/python
# -*- coding: utf-8 -*-

from MyHearthStone import ext
from MyHearthStone.ext import Spell, Minion

__author__ = 'fyabc'


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
