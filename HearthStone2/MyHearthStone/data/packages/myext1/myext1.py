#! /usr/bin/python
# -*- coding: utf-8 -*-

"""Package file of MyExtension.md."""

from MyHearthStone.ext import Minion
from MyHearthStone.ext import blank_minion
from MyHearthStone.ext import std_events
from MyHearthStone.utils.game import Zone

__author__ = 'fyabc'


class 蓝腮骑士(Minion):
    data = {
        'id': "D00000007",
        'rarity': 1, 'cost': 3, 'attack': 2, 'health': 1,
    }

    def run_deathrattle(self, **kwargs):
        location = kwargs.pop('location', 'last')
        return std_events.pure_summon_events(self.game, 7, self.player_id, loc=location)

