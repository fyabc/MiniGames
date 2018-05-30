#! /usr/bin/python
# -*- coding: utf-8 -*-

from MyHearthStone import ext
from MyHearthStone.ext import Weapon, Minion
from MyHearthStone.ext import std_events, std_triggers
from MyHearthStone.utils.game import Type

__author__ = 'fyabc'


###############
# Warrior (8) #
###############


# 暴乱狂战士 (1090007)
Enc_暴乱狂战士 = ext.create_enchantment({'id': 1090003}, *ext.enc_common.apply_fn_add_attack(1))


class 暴乱狂战士(Minion):
    data = {
        'id': 1090007,
        'rarity': 2, 'klass': 9, 'cost': 3, 'attack': 2, 'health': 4,
    }

    class Trig_暴乱狂战士(std_triggers.Trigger):
        respond = [std_events.Damage]

        def process(self, event: respond[0]):
            if event.target.type == Type.Minion:
                Enc_暴乱狂战士.from_card(event, self.game, self.owner)
            return []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Trig_暴乱狂战士(self.game, self)


# 血吼 (1090013)
class 血吼(Weapon):
    data = {
        'id': 1090013,
        'type': 2, 'rarity': 3, 'klass': 9, 'cost': 7, 'attack': 7, 'health': 1,
    }
