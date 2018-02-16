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
    Cost Ascending
    Attack Ascending
    Health Ascending

Default:
    Type = 0
    Rarity = 0
    Klass = 0
    Race = []
    Cost = 0
    Attack = 1
    Health = 1
    Armor = 5

Data dict (`data`) format:
```
data = {
    'id': 6,                                # id, package
    'cost': 2, 'attack': 1, 'health': 1,    # type, klass, rarity, cost, attack, health, armor
    'battlecry': True,                      # other attributes
}
```

Hero ID format:

01 0004
^  ^
|  |
|  Hero ID
|
Package ID

Default:
    Klass = 0
    Health = 30

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
from MyHearthStone.utils.game import Zone, Race

# Load other implementation modules.
# noinspection PyUnresolvedReferences
from impl.basic_enchantments import *

__author__ = 'fyabc'

PackageID = 0


###############
# Neutral (0) #
###############

class 工程师学徒(Minion):
    data = {
        'id': 6,
        'cost': 2, 'attack': 1, 'health': 1,
        'battlecry': True,
    }

    def run_battlecry(self, target):
        return [std_events.DrawCard(self.game, self, self.player_id)]


class 鱼人猎潮者(Minion):
    data = {
        'id': 8,
        'cost': 2, 'attack': 2, 'health': 1,
        'race': [Race.Murloc], 'battlecry': True,
    }

    def run_battlecry(self, target):
        derivative_id = 44  # 鱼人斥候
        game = self.game
        loc = 1 + game.get_zone(Zone.Play, self.player_id).index(self)
        return std_events.pure_summon_events(
            game, minion=derivative_id, to_player=self.player_id, loc=loc,
            from_player=None, from_zone=None)


# 淡水鳄
blank_minion({
    'id': 11,
    'cost': 2, 'attack': 2, 'health': 3,
    'race': [Race.Beast],
})


# 绿洲钳嘴龟
blank_minion({
    'id': 26,
    'cost': 4, 'attack': 2, 'health': 7,
    'race': [Race.Beast],
})


# Neutral derivations.

class 幸运币(Spell):
    data = {
        'id': 43,
        'type': 1, 'rarity': -1, 'cost': 0,
    }

    def run(self, target):
        self.game.add_mana(1, 'T', self.player_id)
        msg.verbose('Add 1 mana to player {} in this turn!'.format(self.player_id))
        return []


# 鱼人斥候
blank_minion({
    'id': 44,
    'rarity': -1, 'cost': 1, 'attack': 1, 'health': 1,
    'race': [Race.Murloc],
})


#############
# Druid (1) #
#############

# 埃隆巴克保护者
blank_minion({
    'id': 10000,
    'klass': 1, 'cost': 8, 'attack': 8, 'health': 8,
    'taunt': True,
})


############
# Mage (3) #
############

class 火球术(Spell):
    data = {
        'id': 30007,
        'type': 1, 'klass': 3, 'cost': 4,
        'have_target': True,
    }

    def run(self, target):
        return std_events.damage_events(self.game, self, target, 6)


###############
# Paladin (4) #
###############


class 力量祝福(Spell):
    data = {
        'id': 40001,
        'type': 1, 'klass': 4, 'cost': 1,
        'have_target': True,
    }

    def check_target(self, target):
        # todo: Extract this checker into an utility function.
        if not super().check_target(target):
            return False

        if target.zone != Zone.Play:
            return False

        return True

    def run(self, target):
        # todo
        return []


#############
# Rogue (6) #
#############

class 影袭(Spell):
    data = {
        'id': 60002,
        'type': 1, 'klass': 6, 'cost': 1,
    }

    def run(self, target):
        return std_events.damage_events(self.game, self, self.game.get_entity(Zone.Hero, 1 - self.player_id), 3)


###############
# Warrior (9) #
###############

# 炽炎战斧
blank_weapon({
    'id': 90008,
    'type': 2, 'klass': 9, 'cost': 3, 'attack': 3, 'health': 2,
})


##########
# Heroes #
##########

class StdDruid(Hero):
    data = {
        'id': 0,
        'klass': 1,
    }


class StdHunter(Hero):
    data = {
        'id': 1,
        'klass': 2,
    }


class StdMage(Hero):
    data = {
        'id': 2,
        'klass': 3,
    }


class StdPaladin(Hero):
    data = {
        'id': 3,
        'klass': 4,
    }


class Priest(Hero):
    data = {
        'id': 4,
        'klass': 5,
    }


class Rogue(Hero):
    data = {
        'id': 5,
        'klass': 6,
    }


class Shaman(Hero):
    data = {
        'id': 6,
        'klass': 7,
    }


class Warlock(Hero):
    data = {
        'id': 7,
        'klass': 8,
    }


class Warrior(Hero):
    data = {
        'id': 8,
        'klass': 9,
    }
