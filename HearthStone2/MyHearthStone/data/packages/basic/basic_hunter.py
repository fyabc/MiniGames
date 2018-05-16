#! /usr/bin/python
# -*- coding: utf-8 -*-

from MyHearthStone import ext
from MyHearthStone.ext import blank_minion
from MyHearthStone.ext import enc_common
from MyHearthStone.ext import std_events
from MyHearthStone.ext import Spell

__author__ = 'fyabc'


##############
# Hunter (2) #
##############

# 森林狼 (20000)

# 驯兽师 (20001)

# 苔原犀牛 (20002)

# 饥饿的秃鹫 (20003)


# 猎人印记 (20004)
Enc_猎人印记 = ext.create_enchantment({'id': 20003}, *enc_common.apply_fn_set_health(1))


class 猎人印记(Spell):
    data = {
        'id': 20004,
        'type': 1, 'klass': 2, 'cost': 1,
        'have_target': True,
    }

    check_target = ext.checker_minion

    def run(self, target, **kwargs):
        Enc_猎人印记.from_card(self, self.game, target)
        return []


# 奥术射击 (20005)
class 奥术射击(Spell):
    data = {
        'id': 20005,
        'type': 1, 'klass': 2, 'cost': 1,
        'have_target': True,
    }

    run = ext.damage_fn(2)


# 追踪术 (20006)

# 动物伙伴 (20007)

# 杀戮命令 (20008)

# 多重射击 (20009)
