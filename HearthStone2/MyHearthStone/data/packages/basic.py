#! /usr/bin/python
# -*- coding: utf-8 -*-

"""Basic package, include basic cards and heroes.

Card ID format:

01 02 0014
^  ^  ^
|  |  |
|  |  Card ID
|  |
|  Class ID
|
Package ID
"""

from MyHearthStone.ext import Minion, Spell, Weapon, Hero
from MyHearthStone.ext import blank_minion, blank_weapon
from MyHearthStone.ext import std_events, std_triggers
from MyHearthStone.ext import message as msg

__author__ = 'fyabc'


###########
# Neutral #
###########

class 幸运币(Spell):
    _data = {
        'id': 0,
        'name': '幸运币',
        'type': 1,
        'rarity': -1,
        'CAH': [0],
    }

    def run(self, target):
        self.game.add_mana(1, '1', self.player_id)
        msg.verbose('Add 1 mana to player {} in this turn!'.format(self.player_id))

        return []


class 工程师学徒(Minion):
    _data = {
        'id': 1,
        'name': '工程师学徒',
        'rarity': 0,
        'CAH': [2, 1, 1],
        'battlecry': True,
    }

    def battlecry(self, target):
        return [std_events.DrawCard(self.game, self, self.player_id)]


淡水鳄 = blank_minion({
    'id': 2,
    'name': '淡水鳄',
    'rarity': 0,
    'CAH': [2, 2, 3],
    'race': [0],
})

########
# Mage #
########


class 火球术(Spell):
    _data = {
        'id': 30004,
        'name': '火球术',
        'type': 1,
        'rarity': 0,
        'klass': 3,
        'CAH': [4],
    }

    have_target = True

    def run(self, target):
        return [std_events.damage_events(self.game, self, target, 6)]


###########
# Warrior #
###########

炽炎战斧 = blank_weapon({
    'id': 90001,
    'name': '炽炎战斧',
    'type': 2,
    'klass': 9,
    'rarity': 0,
    'CAH': [3, 3, 2],
})


##########
# Heroes #
##########


class StdDruid(Hero):
    _data = {
        'id': 0,
        'name': '玛法里奥·怒风',
        'klass': 1,
        'CAH': [None, None, 30],
    }


class StdHunter(Hero):
    _data = {
        'id': 1,
        'name': '雷克萨',
        'klass': 2,
        'CAH': [None, None, 30],
    }


class StdMage(Hero):
    _data = {
        'id': 2,
        'name': '吉安娜·普罗德摩尔',
        'klass': 3,
        'CAH': [None, None, 30],
    }


class StdPaladin(Hero):
    _data = {
        'id': 3,
        'name': '乌瑟尔·光明使者',
        'klass': 4,
        'CAH': [None, None, 30],
    }


class Priest(Hero):
    _data = {
        'id': 4,
        'name': '安度因·乌瑞恩',
        'klass': 5,
        'CAH': [None, None, 30],
    }


class Rogue(Hero):
    _data = {
        'id': 5,
        'name': '瓦莉拉·萨古纳尔',
        'klass': 6,
        'CAH': [None, None, 30],
    }


class Shaman(Hero):
    _data = {
        'id': 6,
        'name': '萨尔',
        'klass': 7,
        'CAH': [None, None, 30],
    }


class Warlock(Hero):
    _data = {
        'id': 7,
        'name': '古尔丹',
        'klass': 8,
        'CAH': [None, None, 30],
    }


class Warrior(Hero):
    _data = {
        'id': 8,
        'name': '加尔鲁什·地狱咆哮',
        'klass': 9,
        'CAH': [None, None, 30],
    }
