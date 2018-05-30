#! /usr/bin/python
# -*- coding: utf-8 -*-

"""This is a package for some new-features test cards."""

from MyHearthStone import ext
from MyHearthStone.ext import Minion
from MyHearthStone.ext import blank_minion
from MyHearthStone.ext import std_events, std_triggers
from MyHearthStone.utils.game import Zone

__author__ = 'fyabc'


class TestDiscardHand(Minion):
    """战吼：选择一张手牌，将其弃置。"""
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


class TestPredamage(Minion):
    """该随从每次只能受到1点伤害。"""
    data = {
        'id': "T00000001",
        'rarity': 2, 'cost': 3, 'attack': 2, 'health': 4,
    }

    class Trig_Predamage(std_triggers.Trigger):
        respond = [std_events.Damage]
        timing = [std_triggers.Trigger.Before]

        def process(self, event: respond[0]):
            if event.target == self.owner:
                event.value = 1
            return []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Trig_Predamage(self.game, self)
