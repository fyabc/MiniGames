#! /usr/bin/python
# -*- coding: utf-8 -*-

from MyHearthStone import ext
from MyHearthStone.ext import Minion, Spell, Hero, HeroPower
from MyHearthStone.ext import std_events
from MyHearthStone.utils.game import Race

__author__ = 'fyabc'


##############
# Shaman (7) #
##############

# Shaman (6)
class Shaman(Hero):
    data = {
        'id': 6,
        'klass': 7, 'hero_power': 6
    }


class 图腾召唤(HeroPower):
    data = {
        'id': 6,
        'klass': 7, 'is_basic': True, 'cost': 2,
        'have_target': False,
    }

    def run(self, target, **kwargs):
        # TODO
        return []

    def can_do_action(self, msg_fn=None):
        super_result = super().can_do_action(msg_fn=msg_fn)
        if super_result == self.Inactive:
            return super_result
        # TODO: Require space, and not all 4 totems
        return super_result


# 火舌图腾 (70000)

# 风语者 (70001)

# 火元素 (70002)

# 先祖治疗 (70003)

# 图腾之力 (70004)

# 冰霜震击 (70005)

# 石化武器 (70006)

# 风怒 (70007)

# 妖术 (70008)

# 嗜血 (70009)


# Derivatives

# 石爪图腾 (70010)
ext.blank_minion({
    'id': 70010,
    'rarity': -1, 'klass': 7, 'cost': 1, 'attack': 0, 'health': 2,
    'race': [Race.Totem], 'derivative': True, 'taunt': True,
})


# 治疗图腾 (70011)
class 治疗图腾(Minion):
    data = {
        'id': 70011,
        'rarity': -1, 'klass': 7, 'cost': 1, 'attack': 0, 'health': 2,
        'race': [Race.Totem], 'derivative': True,
    }

    # TODO


# 空气之怒图腾 (70012)
ext.blank_minion({
    'id': 70012,
    'rarity': -1, 'klass': 7, 'cost': 1, 'attack': 0, 'health': 2,
    'race': [Race.Totem], 'derivative': True, 'spell_power': 1,
})


# 灼热图腾 (70013)
ext.blank_minion({
    'id': 70013,
    'rarity': -1, 'klass': 7, 'cost': 1, 'attack': 1, 'health': 1,
    'race': [Race.Totem], 'derivative': True,
})
