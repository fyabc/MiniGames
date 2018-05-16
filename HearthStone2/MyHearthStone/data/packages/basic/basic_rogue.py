#! /usr/bin/python
# -*- coding: utf-8 -*-

from MyHearthStone.ext import Spell
from MyHearthStone.ext import std_events
from MyHearthStone.utils.game import Zone

__author__ = 'fyabc'


#############
# Rogue (6) #
#############

# 背刺 (60000)

# 致命药膏 (60001)

# 影袭 (60002)
class 影袭(Spell):
    data = {
        'id': 60002,
        'type': 1, 'klass': 6, 'cost': 1,
    }

    def run(self, target, **kwargs):
        return std_events.damage_events(self.game, self, self.game.get_entity(Zone.Hero, 1 - self.player_id), 3)

# 毒刃 (60003)

# 闷棍 (60004)

# 刀扇 (60005)

# 刺杀 (60006)

# 消失 (60007)

# 疾跑 (60008)

# 刺客之刃 (60009)
