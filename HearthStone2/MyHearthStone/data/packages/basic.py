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
from MyHearthStone.ext import blank_minion
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
        'id': 20004,
        'name': '火球术',
        'rarity': 0,
        'CAH': [4],
    }

    have_target = True

    def run(self, target):
        return [std_events.damage_events(self.game, self, target, 6)]


##########
# Heroes #
##########


class Druid(Hero):
    _data = {
        'id': 0,
        'CAH': [None, None, 30],
    }


class Hunter(Hero):
    _data = {
        'id': 1,
        'CAH': [None, None, 30],
    }


class Mage(Hero):
    _data = {
        'id': 2,
        'CAH': [None, None, 30],
    }


class Paladin(Hero):
    _data = {
        'id': 3,
        'CAH': [None, None, 30],
    }


class Priest(Hero):
    _data = {
        'id': 4,
        'CAH': [None, None, 30],
    }


class Rogue(Hero):
    _data = {
        'id': 5,
        'CAH': [None, None, 30],
    }


class Shaman(Hero):
    _data = {
        'id': 6,
        'CAH': [None, None, 30],
    }


class Warlock(Hero):
    _data = {
        'id': 7,
        'CAH': [None, None, 30],
    }


class Warrior(Hero):
    _data = {
        'id': 8,
        'CAH': [None, None, 30],
    }
