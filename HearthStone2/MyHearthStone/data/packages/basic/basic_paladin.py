#! /usr/bin/python
# -*- coding: utf-8 -*-

from MyHearthStone import ext
from MyHearthStone.ext import Minion, Spell, Hero, HeroPower
from MyHearthStone.ext import std_events
from MyHearthStone.ext import enc_common
from MyHearthStone.utils.game import Zone

__author__ = 'fyabc'


###############
# Paladin (4) #
###############

# Paladin (3)
class StdPaladin(Hero):
    data = {
        'id': 3,
        'klass': 4, 'hero_power': 3,
    }


class 援军(HeroPower):
    data = {
        'id': 3,
        'klass': 4, 'is_basic': True, 'cost': 2,
        'have_target': False,
    }

    can_do_action = ext.require_board_not_full

    def run(self, target, **kwargs):
        return std_events.pure_summon_events(self.game, "40010", self.player_id, 'last')


# 列王守卫 (40000)
class 列王守卫(Minion):
    data = {
        'id': 40000,
        'klass': 4, 'cost': 7, 'attack': 5, 'health': 6,
        'battlecry': True,
    }

    def run_battlecry(self, target, **kwargs):
        return [std_events.Healing(self.game, self, self.game.get_hero(self.player_id), 6)]


# 力量祝福 (40001)
Enc_力量祝福 = ext.create_enchantment({'id': 40000}, *enc_common.apply_fn_add_attack(3))


class 力量祝福(Spell):
    data = {
        'id': 40001,
        'type': 1, 'klass': 4, 'cost': 1,
        'have_target': True,
    }

    check_target = ext.checker_minion

    def run(self, target, **kwargs):
        Enc_力量祝福.from_card(self, self.game, target)
        return []


# 保护之手 (40002)

# 谦逊 (40003)

# 圣光术 (40004)

# 王者祝福 (40005)
Enc_王者祝福 = ext.create_enchantment({'id': 40003}, *enc_common.apply_fn_add_a_h(4, 4))


class 王者祝福(Spell):
    data = {
        'id': 40005,
        'type': 1, 'klass': 4, 'cost': 4,
        'have_target': True,
    }

    check_target = ext.checker_minion

    def run(self, target, **kwargs):
        Enc_王者祝福.from_card(self, self.game, target)
        return []

# 奉献 (40006)

# 愤怒之锤 (40007)

# 圣光的正义 (40008)

# 真银圣剑 (40009)


# Derivatives

# 白银之手新兵 (40010)
ext.blank_minion({
    'id': 40010,
    'rarity': -1, 'klass': 4, 'cost': 1, 'attack': 1, 'health': 1,
    'derivative': True,
})
