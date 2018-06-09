#! /usr/bin/python
# -*- coding: utf-8 -*-

from MyHearthStone import ext
from MyHearthStone.ext import Minion, Spell, Hero, HeroPower
from MyHearthStone.ext import Aura
from MyHearthStone.ext import std_events
from MyHearthStone.utils.game import Type, DHBonusType, DHBonusEventType, AuraType

__author__ = 'fyabc'


##############
# Priest (5) #
##############

class Enc_先知维伦(ext.DHBonusAuraEnchantment):
    data = {
        'id': 1050000,
    }

    event_types = [DHBonusEventType.Damage, DHBonusEventType.Healing]
    source_types = [Type.Spell, Type.HeroPower]
    bonus_types = [DHBonusType.Double]

    def get_bonus_value(self):
        return 1


# 先知维伦 (1050014)
class 先知维伦(Minion):
    """[NOTE]: This is a classic card of damage/healing bonus effects."""
    data = {
        'id': 1050014,
        'rarity': 4, 'klass': 5, 'cost': 7, 'attack': 7, 'health': 7,
    }

    class Aura_先知维伦(Aura):
        type = AuraType.Other

        def check_entity(self, entity, **kwargs):
            return entity.type == Type.Player and entity.player_id == self.owner.player_id

        def grant_enchantment(self, entity, **kwargs):
            Enc_先知维伦.from_card(self.owner, self.game, entity, self)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Aura_先知维伦(self.game, self)
