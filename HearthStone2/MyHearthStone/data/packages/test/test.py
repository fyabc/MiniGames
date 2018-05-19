#! /usr/bin/python
# -*- coding: utf-8 -*-

"""This is a package for some new-features test cards."""

from MyHearthStone import ext
from MyHearthStone.ext import Minion
from MyHearthStone.ext import blank_minion
from MyHearthStone.ext import std_events
from MyHearthStone.utils.game import Zone

__author__ = 'fyabc'


class TestDiscardHand(Minion):
    data = {
        'id': "T00000000",
        'rarity': 1, 'cost': 1, 'attack': 2, 'health': 1,
    }

    check_target = ext.checker_my_hand

    @property
    def have_target(self):
        my_hand = self.game.get_zone(Zone.Hand, self.player_id)
        if self in my_hand:
            return len(my_hand) >= 2
        else:
            return bool(my_hand)

    def run_battlecry(self, target, **kwargs):
        return [std_events.DiscardCard(self.game, self, target)]
