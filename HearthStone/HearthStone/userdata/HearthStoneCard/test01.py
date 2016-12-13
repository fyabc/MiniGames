#! /usr/bin/python
# -*- coding: utf-8 -*-

from HearthStone.ext import Minion, set_description
from HearthStone.ext import DrawCard, AddMinionToDesk, Damage
from HearthStone.ext import random_card

__author__ = 'fyabc'


Package = {
    'id': 101,     # id > 100 is user package
    'name': 'Test01',
}


###################
# Neutral Minions #
###################

class 随机1(Minion):
    _data = dict(id=101000, name='随机1', CAH=[4, 2, 2], rarity=4)

    def run_battle_cry(self, player_id, location):
        self.game.add_event_quick(AddMinionToDesk, random_card(), location + 1, player_id)


class 随机2(Minion):
    _data = dict(id=101001, name='随机2', CAH=[6, 4, 2], rarity=4)

    def run_battle_cry(self, player_id, location):
        self.game.add_event_quick(AddMinionToDesk, random_card('rarity = 4'), location + 1, player_id)


set_description({
    随机1: '战吼：随机召唤一个随从。',
    随机2: '战吼：随机召唤一个传说随从。',
})
