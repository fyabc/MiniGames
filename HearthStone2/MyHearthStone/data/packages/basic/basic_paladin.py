#! /usr/bin/python
# -*- coding: utf-8 -*-

from MyHearthStone import ext
from MyHearthStone.ext import Spell

__author__ = 'fyabc'


###############
# Paladin (4) #
###############

# 列王守卫 (40000)

# 力量祝福 (40001)
def _apply(self):
    self.target.data['attack'] += 3


# [NOTE]: Must assign this to a global variable, or use ``add_to_module`` argument.
Enc_力量祝福 = ext.create_enchantment({'id': 40000}, apply_fn=_apply)


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
def _apply(self):
    self.target.data['attack'] += 4
    self.target.inc_health(4)


Enc_王者祝福 = ext.create_enchantment({'id': 40003}, apply_fn=_apply)


class 王者祝福(Spell):
    data = {
        'id': 40005,
        'type': 1, 'klass': 4, 'cost': 4,
        'have_target': True
    }

    check_target = ext.checker_minion

    def run(self, target, **kwargs):
        Enc_王者祝福.from_card(self, self.game, target)
        return []

# 奉献 (40006)

# 愤怒之锤 (40007)

# 圣光的正义 (40008)

# 真银圣剑 (40009)
