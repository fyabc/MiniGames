#! /usr/bin/python
# -*- coding: utf-8 -*-

from random import choice

from MyHearthStone import ext
from MyHearthStone.ext import Minion, Spell, Hero, HeroPower
from MyHearthStone.ext import std_events
from MyHearthStone.utils.game import Race, Zone

__author__ = 'fyabc'


###############
# Warlock (8) #
###############

# Warlock (7)
class Warlock(Hero):
    data = {
        'id': 7,
        'klass': 8, 'hero_power': 7,
    }


class 生命分流(HeroPower):
    data = {
        'id': 7,
        'klass': 8, 'is_basic': True, 'cost': 2,
        'have_target': False,
    }
    ext.add_dh_bonus_data(data, 2)

    def run(self, target, **kwargs):
        return [std_events.Damage(self.game, self, target=self.game.get_hero(self.player_id), value=self.dh_values[0]),
                std_events.DrawCard(self.game, self, self.player_id)]


# 虚空行者 (80000)
ext.blank_minion({
    'id': 80000,
    'klass': 8, 'cost': 1, 'attack': 1, 'health': 3,
    'taunt': True, 'race': [Race.Demon],
})


# 魅魔 (80001)
class 魅魔(Minion):
    data = {
        'id': 80001,
        'klass': 8, 'cost': 2, 'attack': 4, 'health': 3,
        'battlecry': True, 'race': [Race.Demon],
    }

    def run_battlecry(self, target, **kwargs):
        target = choice(self.game.get_zone(Zone.Hand, self.player_id))
        return [std_events.DiscardCard(self.game, self, target)]


# 恐惧地狱火 (80002)

# 牺牲契约 (80003)

# 灵魂之火 (80004)

# 死亡缠绕 (80005)

# 腐蚀术 (80006)


# 吸取生命 (80007)
class 吸取生命(Spell):
    data = {
        'id': 80007,
        'type': 1, 'klass': 8, 'cost': 3,
        'have_target': True,
    }
    ext.add_dh_bonus_data(data, [2, 2])

    def run(self, target, **kwargs):
        # TODO
        return []


# 暗影箭 (80008)
class 暗影箭(Spell):
    data = {
        'id': 80008,
        'type': 1, 'klass': 8, 'cost': 3,
        'have_target': True,
    }
    ext.add_dh_bonus_data(data, 4)

    can_do_action = ext.require_minion
    check_target = ext.checker_minion

    def run(self, target, **kwargs):
        return [std_events.Damage(self.game, self, target, self.dh_values[0])]


# 地狱烈焰 (80009)
class 地狱烈焰(Spell):
    data = {
        'id': 80009,
        'type': 1, 'klass': 8, 'cost': 4,
    }
    ext.add_dh_bonus_data(data, 3)

    def run(self, target, **kwargs):
        targets = ext.collect_all(self, False, oop=True)
        return [std_events.AreaDamage(self.game, self, targets, [self.dh_values[0] for _ in targets])]
