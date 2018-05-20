#! /usr/bin/python
# -*- coding: utf-8 -*-

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

    def run(self, target, **kwargs):
        return [std_events.Damage(self.game, self, target=self.game.get_zone(Zone.Hero, self.player_id)[0], value=2),
                std_events.DrawCard(self.game, self, self.player_id)]


# 虚空行者 (80000)
ext.blank_minion({
    'id': 80000,
    'klass': 8, 'cost': 1, 'attack': 1, 'health': 3,
    'taunt': True, 'race': [Race.Demon],
})

# 魅魔 (80001)

# 恐惧地狱火 (80002)

# 牺牲契约 (80003)

# 灵魂之火 (80004)

# 死亡缠绕 (80005)

# 腐蚀术 (80006)

# 吸取生命 (80007)

# 暗影箭 (80008)

# 地狱烈焰 (80009)
