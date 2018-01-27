#! /usr/bin/python
# -*- coding: utf-8 -*-

"""Basic package, include basic cards and heroes.

All ID start from 0.

Card ID format:

01 02 0014
^  ^  ^
|  |  |
|  |  Card ID
|  |
|  Class ID
|
Package ID

Ordered by:
    Package
    Class
    Rarity (Basic -> Common -> Rare -> Epic -> Legend -> Derivative
    Type (Minion -> Spell -> Weapon -> HeroCard)
    Cost (CAH[0]) Ascending
    Attack (CAH[1]) Ascending
    Health (CAH[2]) Ascending

Default:
    Type = 0
    Rarity = 0
    Klass = 0
    Race = []
    CAH = [0, 1, 1]

Hero ID format:

01 0004
^  ^
|  |
|  Hero ID
|
Package ID

Default:
    Klass = 0
    CAH = [None, None, 30]

Enchantment ID format:

01 0004
^  ^
|  |
|  Enchantment ID
|
Package ID
"""

from MyHearthStone.ext import Minion, Spell, Hero
from MyHearthStone.ext import blank_minion, blank_weapon
from MyHearthStone.ext import std_events
from MyHearthStone.ext import message as msg

# Load other implementation modules.
# noinspection PyUnresolvedReferences
from impl.basic_enchantments import *

__author__ = 'fyabc'

PackageID = 0


###############
# Neutral (0) #
###############

class 工程师学徒(Minion):
    _data = {
        'id': 6,
        'CAH': [2, 1, 1],
        'battlecry': True,
    }

    def battlecry(self, target):
        return [std_events.DrawCard(self.game, self, self.player_id)]


# 淡水鳄
blank_minion({
    'id': 11,
    'CAH': [2, 2, 3],
    'race': [0],
})


# Neutral derivations.

class 幸运币(Spell):
    _data = {
        'id': 43,
        'type': 1, 'rarity': -1, 'CAH': [0],
    }

    def run(self, target):
        self.game.add_mana(1, 'T', self.player_id)
        msg.verbose('Add 1 mana to player {} in this turn!'.format(self.player_id))
        return []


#############
# Druid (1) #
#############

# 埃隆巴克保护者
blank_minion({
    'id': 10000,
    'CAH': [8, 8, 8],
    'taunt': True,
})


############
# Mage (3) #
############

class 火球术(Spell):
    _data = {
        'id': 30007,
        'type': 1, 'klass': 3, 'CAH': [4],
        'have_target': True,
    }

    def run(self, target):
        return [std_events.damage_events(self.game, self, target, 6)]


###############
# Warrior (9) #
###############

# 炽炎战斧
blank_weapon({
    'id': 90008,
    'type': 2, 'klass': 9, 'CAH': [3, 3, 2],
})


##########
# Heroes #
##########

class StdDruid(Hero):
    _data = {
        'id': 0,
        'klass': 1,
    }


class StdHunter(Hero):
    _data = {
        'id': 1,
        'klass': 2,
    }


class StdMage(Hero):
    _data = {
        'id': 2,
        'klass': 3,
    }


class StdPaladin(Hero):
    _data = {
        'id': 3,
        'klass': 4,
    }


class Priest(Hero):
    _data = {
        'id': 4,
        'klass': 5,
    }


class Rogue(Hero):
    _data = {
        'id': 5,
        'klass': 6,
    }


class Shaman(Hero):
    _data = {
        'id': 6,
        'klass': 7,
    }


class Warlock(Hero):
    _data = {
        'id': 7,
        'klass': 8,
    }


class Warrior(Hero):
    _data = {
        'id': 8,
        'klass': 9,
    }
