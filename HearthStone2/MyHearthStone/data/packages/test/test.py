#! /usr/bin/python
# -*- coding: utf-8 -*-

"""This is a package for some new-features test cards."""

from MyHearthStone import ext
from MyHearthStone.ext import Minion, Spell
from MyHearthStone.ext import blank_minion
from MyHearthStone.ext import std_events, std_triggers
from MyHearthStone.utils.game import Zone

__author__ = 'fyabc'


def _cond_fn(self):
    my_hand = self.game.get_zone(Zone.Hand, self.player_id)
    if self in my_hand:
        return len(my_hand) >= 2
    else:
        return bool(my_hand)


# TODO: Add card names into test card docstrings.


class TestDiscardHand(Minion):
    """战吼：选择一张手牌，将其弃置。"""
    data = {
        'id': "T00000000",
        'rarity': 1, 'cost': 1, 'attack': 2, 'health': 1,
    }

    check_target = ext.checker_my_hand

    player_operation_tree = ext.make_conditional_targeted_po_tree(_cond_fn)

    def run_battlecry(self, target, **kwargs):
        return [std_events.DiscardCard(self.game, self, target)]


class TestPredamage(Minion):
    """该随从每次只能受到1点伤害。"""
    data = {
        'id': "T00000001",
        'rarity': 2, 'cost': 3, 'attack': 2, 'health': 4,
    }

    class Trig_Predamage(std_triggers.AttachedTrigger):
        respond = [std_events.Damage]
        timing = [std_triggers.Trigger.Before]

        def process(self, event: respond[0]):
            if event.target == self.owner:
                event.value = 1
            return []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Trig_Predamage(self.game, self)


class QuickGetMana(Spell):
    """在本回合中，获得十个法力水晶。"""
    data = {
        'id': "T00000002",
        'type': 1, 'rarity': 0, 'cost': 0,
    }

    def run(self, target, **kwargs):
        self.game.add_mana(10, 'T', self.player_id)
        return []


class QuickDamage(Spell):
    """对敌方英雄造成100点伤害。"""
    data = {
        'id': "T00000003",
        'type': 1, 'rarity': 0, 'cost': 0,
    }
    ext.add_dh_bonus_data(data, 100)

    def run(self, target, **kwargs):
        return [std_events.Damage(self.game, self, self.game.get_hero(1 - self.player_id), self.dh_values[0])]


class TestCopy(Spell):
    """选择一个随从，召唤它的一个复制。"""
    data = {
        'id': "T00000004",
        'type': 1, 'rarity': 0, 'cost': 0,
        'po_tree': '$HaveTarget',
    }

    can_do_action = ext.require_minion
    check_target = ext.checker_minion

    def run(self, target, **kwargs):
        return std_events.pure_summon_events(self.game, target, self.player_id, 'last', copy=True)
