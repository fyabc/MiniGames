#! /usr/bin/python
# -*- coding: utf-8 -*-

from MyHearthStone import ext
from MyHearthStone.ext import Spell, Hero, HeroPower
from MyHearthStone.ext import std_events
from MyHearthStone.utils.game import Zone

__author__ = 'fyabc'


#############
# Rogue (6) #
#############

# Rogue (5)
class Rogue(Hero):
    data = {
        'id': 5,
        'klass': 6, 'hero_power': 5,
    }


class 匕首精通(HeroPower):
    data = {
        'id': 5,
        'klass': 6, 'is_basic': True, 'cost': 2,
        'have_target': False,
    }

    def run(self, target, **kwargs):
        # TODO
        return []


# 背刺 (60000)

# 致命药膏 (60001)

# 影袭 (60002)
class 影袭(Spell):
    data = {
        'id': 60002,
        'type': 1, 'klass': 6, 'cost': 1,
    }

    def run(self, target, **kwargs):
        return [std_events.Damage(self.game, self, self.game.get_hero(1 - self.player_id), 3)]


# 毒刃 (60003)
class 毒刃(Spell):
    data = {
        'id': 60003,
        'type': 1, 'klass': 6, 'cost': 2,
        'have_target': True,
    }

    def run(self, target, **kwargs):
        return [std_events.Damage(self.game, self, target, 1), std_events.DrawCard(self.game, self, self.player_id)]


# 闷棍 (60004)
class 闷棍(Spell):
    data = {
        'id': 60004,
        'type': 1, 'klass': 6, 'cost': 2,
        'have_target': True,
    }

    check_target = ext.checker_enemy_minion

    def run(self, target, **kwargs):
        _, status = self.game.move(target.player_id, target.zone, target, target.player_id, Zone.Hand, 'last')
        return status['events']

# 刀扇 (60005)

# 刺杀 (60006)

# 消失 (60007)

# 疾跑 (60008)

# 刺客之刃 (60009)


# Derivatives

# 邪恶短刀 (60010)
ext.blank_weapon({
    'id': 60010,
    'rarity': -1, 'type': 2, 'klass': 6, 'cost': 1, 'attack': 1, 'health': 2,
    'derivative': True,
})
