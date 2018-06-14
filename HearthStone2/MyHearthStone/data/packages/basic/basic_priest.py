#! /usr/bin/python
# -*- coding: utf-8 -*-

from MyHearthStone import ext
from MyHearthStone.ext import Minion, Spell, Hero, HeroPower
from MyHearthStone.ext import std_events
from MyHearthStone.utils.game import Zone

__author__ = 'fyabc'


##############
# Priest (5) #
##############

# Priest (4)
class Priest(Hero):
    data = {
        'id': 4,
        'klass': 5, 'hero_power': 4,
    }


class 次级治疗术(HeroPower):
    data = {
        'id': 4,
        'klass': 5, 'is_basic': True, 'cost': 2,
        'have_target': True,
    }
    ext.add_dh_bonus_data(data, 2)

    def run(self, target, **kwargs):
        return [std_events.Healing(self.game, self, target, self.dh_values[0])]


# 北郡牧师 (50000)

# 神圣惩击 (50001)

# 心灵视界 (50002)

# 真言术：盾 (50003)

# 神圣之灵 (50004)

# 心灵震爆 (50005)

# 暗言术：痛 (50006)

# 暗言术：灭 (50007)

# 神圣新星 (50008)


# 精神控制 (50009)
class 精神控制(Spell):
    """[NOTE]: This is a classic card of (permanent) mind control effect."""
    data = {
        'id': 50009,
        'type': 1, 'klass': 5, 'cost': 10,
        'have_target': True,
    }

    can_do_action = ext.require_board_not_full
    check_target = ext.checker_enemy_minion

    def run(self, target, **kwargs):
        entity, status = self.game.move(target.player_id, target.zone, target, self.player_id, Zone.Play, 'last')
        return status['events']
