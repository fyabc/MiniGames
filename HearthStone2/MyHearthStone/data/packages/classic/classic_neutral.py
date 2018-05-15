#! /usr/bin/python
# -*- coding: utf-8 -*-

"""Classic package."""

from MyHearthStone import ext
from MyHearthStone.ext import blank_minion
from MyHearthStone.ext import Minion, Spell, Weapon, Enchantment
from MyHearthStone.ext import std_events, std_triggers
from MyHearthStone.utils.game import Race, Zone

__author__ = 'fyabc'


###############
# Neutral (0) #
###############

# 小精灵 (1000000)
blank_minion({
    'id': 1000000,
    'rarity': 1, 'cost': 0, 'attack': 1, 'health': 1,
})

# 持盾卫士 (1000001)
blank_minion({
    'id': 1000001,
    'rarity': 1, 'cost': 1, 'attack': 0, 'health': 4,
    'taunt': True,
})


# 叫嚣的中士 (1000002)
class Enc_叫嚣的中士(Enchantment):
    data = {
        'id': 1000000,
    }

    class Trig_叫嚣的中士(std_triggers.Trigger):
        respond = [std_events.EndOfTurn]

        def process(self, event: respond[0]):
            self.owner.detach(remove_from_target=True)
            return []

    def __init__(self, game, target, **kwargs):
        super().__init__(game, target, **kwargs)
        self.Trig_叫嚣的中士(self.game, self)

    def apply(self):
        self.target.data['attack'] += 2


class 叫嚣的中士(Minion):
    data = {
        'id': 1000002,
        'rarity': 1, 'cost': 1, 'attack': 1, 'health': 1,
    }

    @property
    def have_target(self):
        return bool(self.game.get_zone(Zone.Play, self.player_id)) or \
               bool(self.game.get_zone(Zone.Play, 1 - self.player_id))

    def run_battlecry(self, target, **kwargs):
        if target is not None:
            Enc_叫嚣的中士.from_card(self, self.game, target)
        return []


# 银色侍从 (1000003)
blank_minion({
    'id': 1000003,
    'rarity': 1, 'cost': 1, 'attack': 1, 'health': 1,
    'divine_shield': True,
})

# 幼龙鹰 (1000005)
blank_minion({
    'id': 1000005,
    'rarity': 1, 'cost': 1, 'attack': 1, 'health': 1,
    'windfury': True, 'race': [Race.Beast],
})

# 狼人渗透者 (1000007)
blank_minion({
    'id': 1000007,
    'rarity': 1, 'cost': 1, 'attack': 2, 'health': 1,
    'stealth': True,
})


# 战利品贮藏者 (1000008)
class 战利品贮藏者(Minion):
    data = {
        'id': 1000008,
        'rarity': 1, 'cost': 2, 'attack': 2, 'health': 1,
    }

    def run_deathrattle(self, **kwargs):
        return [std_events.DrawCard(self.game, self, self.player_id)]


# 血色十字军战士 (1000021)
blank_minion({
    'id': 1000021,
    'rarity': 1, 'cost': 3, 'attack': 3, 'health': 1,
    'divine_shield': True,
})
