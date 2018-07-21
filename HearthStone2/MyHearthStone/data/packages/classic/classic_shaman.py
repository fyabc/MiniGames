#! /usr/bin/python
# -*- coding: utf-8 -*-

from MyHearthStone import ext
from MyHearthStone.ext import Spell, Minion
from MyHearthStone.ext import DrEnchantment
from MyHearthStone.ext import std_events, std_triggers

__author__ = 'fyabc'


##############
# Shaman (7) #
##############


class Enc_先祖之魂(DrEnchantment):
    data = {
        'id': 1070001,
    }

    def __init__(self, game, target, **kwargs):
        # Summon a copy of the died minion.
        kwargs['dr_fn'] = lambda trigger, event: std_events.pure_summon_events(
            game, event.owner.id, event.owner.player_id, event.location)
        super().__init__(game, target, **kwargs)


# 先祖之魂(1070007)
class 先祖之魂(Spell):
    """[NOTE]: This is a classic card of deathrattle enchantment."""
    data = {
        'id': 1070007,
        'type': 1, 'rarity': 2, 'klass': 7, 'cost': 2,
        'po_tree': '$HaveTarget',
    }

    can_do_action = ext.require_minion
    check_target = ext.checker_minion

    def run(self, target, **kwargs):
        Enc_先祖之魂.from_card(self, self.game, target)
        return []
