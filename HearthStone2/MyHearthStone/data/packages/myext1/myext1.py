#! /usr/bin/python
# -*- coding: utf-8 -*-

"""Package file of MyExtension.md."""

from MyHearthStone.ext import Minion
from MyHearthStone.ext import blank_minion
from MyHearthStone.ext import std_events, std_triggers
from MyHearthStone.utils.game import Zone, Race

__author__ = 'fyabc'


class 蓝腮骑士(Minion):
    data = {
        'id': "D00000007",
        'rarity': 1, 'cost': 3, 'attack': 2, 'health': 1,
        'race': [Race.Murloc],
    }

    def __init__(self, game, player_id):
        super().__init__(game, player_id)
        # TODO: Change other deathrattle cards like this.
        self.dr_trigger = std_triggers.DrTrigger.create(
            self.game, owner=self,
            dr_fn=lambda trigger, event: std_events.pure_summon_events(
                self.game, "7", self.player_id, loc=event.location),
            reg_fn=None, data=None,
        )
