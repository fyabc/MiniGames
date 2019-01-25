#! /usr/bin/python
# -*- coding: utf-8 -*-

"""Neutral common cards of the classic package."""

from MyHearthStone import ext
from MyHearthStone.ext import blank_minion
from MyHearthStone.ext import Minion
from MyHearthStone.ext import Enchantment, Aura, AuraEnchantment
from MyHearthStone.ext import std_events, std_triggers
from MyHearthStone.ext import enc_common
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

    def __init__(self, game, target, **kwargs):
        super().__init__(game, target, **kwargs)
        std_triggers.DetachOnTurnEnd(self.game, self)

    apply, apply_imm = enc_common.apply_fn_add_attack(2)


class 叫嚣的中士(Minion):
    data = {
        'id': 1000002,
        'rarity': 1, 'cost': 1, 'attack': 1, 'health': 1,
        'battlecry': True,
    }

    player_operation_tree = ext.make_conditional_targeted_po_tree(ext.have_minion)

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


# 麻风侏儒 (1000004)
class 麻风侏儒(Minion):
    data = {
        'id': 1000004,
        'rarity': 1, 'cost': 1, 'attack': 1, 'health': 1,
        'deathrattle': True,
    }

    def __init__(self, game, player_id):
        super().__init__(game, player_id)
        self.dr_trigger = std_triggers.DrTrigger.create(
            self.game, owner=self,
            dr_fn=lambda trigger, event: [
                std_events.Damage(self.game, self, self.game.get_hero(1 - self.player_id), 2)],
            reg_fn=None, data=None,
        )


# 幼龙鹰 (1000005)
blank_minion({
    'id': 1000005,
    'rarity': 1, 'cost': 1, 'attack': 1, 'health': 1,
    'windfury': True, 'race': [Race.Beast],
})


# 南海船工 (1000006)
class 南海船工(Minion):
    data = {
        'id': 1000006,
        'rarity': 1, 'cost': 1, 'attack': 2, 'health': 1,
        'race': [Race.Pirate],
    }

    # TODO


# 狼人渗透者 (1000007)
blank_minion({
    'id': 1000007,
    'rarity': 1, 'cost': 1, 'attack': 2, 'health': 1,
    'stealth': True,
})


# 战利品贮藏者 (1000008)
class 战利品贮藏者(Minion):
    """[NOTE]: This is a classic card of deathrattle."""
    data = {
        'id': 1000008,
        'rarity': 1, 'cost': 2, 'attack': 2, 'health': 1,
        'deathrattle': True,
    }

    def __init__(self, game, player_id):
        super().__init__(game, player_id)
        self.dr_trigger = std_triggers.DrTrigger.create(
            self.game, owner=self,
            dr_fn=lambda trigger, event: [std_events.DrawCard(self.game, self, self.player_id)],
            reg_fn=None, data=None,
        )


# 恐狼前锋 (1000009)
Enc_恐狼前锋 = ext.create_enchantment({'id': 1000002}, *enc_common.apply_fn_add_attack(1), base=AuraEnchantment)


class 恐狼前锋(Minion):
    """[NOTE]: This is a classic card of adjacent aura."""
    data = {
        'id': 1000009,
        'rarity': 1, 'cost': 2, 'attack': 2, 'health': 2,
        'race': [Race.Beast],
    }

    class Aura_恐狼前锋(Aura):
        def __init__(self, game, owner):
            super().__init__(game, owner)
            self.location = None

        def prepare_update(self):
            z, p = self.owner.zone, self.owner.player_id
            self.location = self.game.get_zone(z, p).index(self.owner)

        def check_entity(self, entity, **kwargs):
            return entity.zone == Zone.Play and entity.player_id == self.owner.player_id and \
                abs(kwargs['location'] - self.location) == 1

        def grant_enchantment(self, entity, **kwargs):
            Enc_恐狼前锋.from_card(self.owner, self.game, entity, self)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Aura_恐狼前锋(self.game, self)


# 阿曼尼狂战士 (1000010)
Enc_阿曼尼狂战士 = ext.create_enchantment({'id': 1000003}, *enc_common.apply_fn_add_attack(3), base=AuraEnchantment)


class 阿曼尼狂战士(Minion):
    data = {
        'id': 1000010,
        'rarity': 1, 'cost': 2, 'attack': 2, 'health': 3,
    }

    class Aura_阿曼尼狂战士(Aura):
        def check_entity(self, entity, **kwargs):
            return entity is self.owner

        def grant_enchantment(self, entity, **kwargs):
            Enc_阿曼尼狂战士.from_card(self.owner, self.game, entity, self)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Aura_阿曼尼狂战士(self.game, self)


# 血帆袭击者 (1000011)
class Enc_血帆袭击者(Enchantment):
    data = {
        'id': 1000004,
    }

    def __init__(self, game, target, n, **kwargs):
        super().__init__(game, target, **kwargs)
        self.n = n

    def apply(self):
        self.target.aura_tmp['attack'] += self.n


class 血帆袭击者(Minion):
    data = {
        'id': 1000011,
        'rarity': 1, 'cost': 2, 'attack': 2, 'health': 3,
        'battlecry': True, 'race': [Race.Pirate],
    }

    def run_battlecry(self, target, **kwargs):
        weapon = self.game.get_weapon(self.player_id)
        n = weapon.attack if weapon is not None else 0
        if n > 0:
            Enc_血帆袭击者.from_card(self, self.game, self, n)
        return []


# 精灵龙 (1000012)
blank_minion({
    'id': 1000012,
    'rarity': 1, 'cost': 2, 'attack': 3, 'health': 2,
    'elusive': True, 'race': [Race.Dragon],
})


# 疯狂投弹者 (1000013)


# 血色十字军战士 (1000021)
blank_minion({
    'id': 1000021,
    'rarity': 1, 'cost': 3, 'attack': 3, 'health': 1,
    'divine_shield': True,
})
