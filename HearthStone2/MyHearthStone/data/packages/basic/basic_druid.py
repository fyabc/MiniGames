#! /usr/bin/python
# -*- coding: utf-8 -*-

from MyHearthStone import ext
from MyHearthStone.ext import blank_minion
from MyHearthStone.ext import std_events
from MyHearthStone.ext import Spell

__author__ = 'fyabc'


#############
# Druid (1) #
#############

# 埃隆巴克保护者 (10000)
blank_minion({
    'id': 10000,
    'klass': 1, 'cost': 8, 'attack': 8, 'health': 8,
    'taunt': True,
})


# 月火术 (10001)
class 月火术(Spell):
    data = {
        'id': 10001,
        'type': 1, 'klass': 1, 'cost': 0,
        'have_target': True,
    }

    run = ext.damage_fn(1)


# 激活 (10002)
class 激活(Spell):
    data = {
        'id': 10002,
        'type': 1, 'klass': 1, 'cost': 0,
    }

    def run(self, target, **kwargs):
        self.game.add_mana(1, 'T', self.player_id)
        return []


# 爪击 (10003)


# 野性印记 (10004)
def _apply(self):
    self.target.data['attack'] += 2
    self.target.inc_health(2)
    self.target.taunt = True


Enc_野性印记 = ext.create_enchantment({'id': 10000}, apply_fn=_apply)


class 野性印记(Spell):
    data = {
        'id': 10004,
        'type': 1, 'klass': 1, 'cost': 2,
        'have_target': True,
    }

    check_target = ext.checker_minion

    def run(self, target, **kwargs):
        Enc_野性印记.from_card(self, self.game, target)
        return []

# 野性成长 (10005)


# 治疗之触 (10006)
class 治疗之触(Spell):
    data = {
        'id': 10006,
        'type': 1, 'klass': 1, 'cost': 3,
        'have_target': True,
    }

    def run(self, target, **kwargs):
        return [std_events.Healing(self.game, self, target, 8)]


# 野蛮咆哮 (10007)

# 横扫 (10008)

# 星火术 (10009)
