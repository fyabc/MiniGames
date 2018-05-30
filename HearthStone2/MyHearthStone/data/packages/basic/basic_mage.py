#! /usr/bin/python
# -*- coding: utf-8 -*-

from MyHearthStone import ext
from MyHearthStone.ext import Minion, Spell, Hero, HeroPower
from MyHearthStone.ext import std_events
from MyHearthStone.utils.game import order_of_play, Zone

__author__ = 'fyabc'


############
# Mage (3) #
############

# Mage (2)
class StdMage(Hero):
    data = {
        'id': 2,
        'klass': 3, 'hero_power': 2,
    }


class 火焰冲击(HeroPower):
    data = {
        'id': 2,
        'klass': 3, 'is_basic': True, 'cost': 2,
        'have_target': True,
    }

    def run(self, target, **kwargs):
        return [std_events.Damage(self.game, self, target, 1)]


# 水元素 (30000)

# 奥术飞弹 (30001)


# 镜像 (30002)
class 镜像(Spell):
    data = {
        'id': 30002,
        'type': 1, 'klass': 3, 'cost': 1,
    }

    # TODO: Need test in game, is this requirement correct?
    can_do_action = ext.require_board_not_full

    def run(self, target, **kwargs):
        return std_events.pure_summon_events(self.game, "30010", self.player_id, 'last') + \
               std_events.pure_summon_events(self.game, "30010", self.player_id, 'last')


# 魔爆术 (30003)
class 魔爆术(Spell):
    data = {
        'id': 30003,
        'type': 1, 'klass': 3, 'cost': 2,
    }

    def run(self, target, **kwargs):
        targets = ext.collect_1p_minions(self, False, oop=True, player_id=1 - self.player_id)
        return [std_events.AreaDamage(self.game, self, targets, [1 for _ in targets])]


# 寒冰箭 (30004)
class 寒冰箭(Spell):
    data = {
        'id': 30004,
        'type': 1, 'klass': 3, 'cost': 2,
        'have_target': True,
    }

    def run(self, target, **kwargs):
        return [std_events.Damage(self.game, self, target, 3),
                std_events.Freeze(self.game, self, target)]


# 奥术智慧 (30005)
class 奥术智慧(Spell):
    data = {
        'id': 30005,
        'type': 1, 'klass': 3, 'cost': 3,
    }

    run = ext.draw_card_fn(2)


# 冰霜新星 (30006)

# 火球术 (30007)
class 火球术(Spell):
    data = {
        'id': 30007,
        'type': 1, 'klass': 3, 'cost': 4,
        'have_target': True,
    }

    run = ext.damage_fn(6)


# 变形术 (30008)


# 烈焰风暴 (30009)
class 烈焰风暴(Spell):
    data = {
        'id': 30009,
        'type': 1, 'klass': 3, 'cost': 7,
    }

    def run(self, target, **kwargs):
        targets = ext.collect_1p_minions(self, False, oop=True, player_id=1 - self.player_id)
        return [std_events.AreaDamage(self.game, self, targets, [4 for _ in targets])]


# Derivatives.


# 镜像 (30010)
ext.blank_minion({
    'id': 30010,
    'rarity': -1, 'klass': 3, 'cost': 0, 'attack': 0, 'health': 2,
    'derivative': True, 'taunt': True,
})

# 绵羊 (47) in ``basic_neutral.py``.
