#! /usr/bin/python
# -*- coding: utf-8 -*-

from random import choice

from MyHearthStone import ext
from MyHearthStone.ext import Minion, Spell, Hero, HeroPower
from MyHearthStone.ext import Enchantment, Aura, AuraEnchantment
from MyHearthStone.ext import std_events, std_triggers
from MyHearthStone.ext import enc_common
from MyHearthStone.utils.game import Race, Zone

__author__ = 'fyabc'


##############
# Shaman (7) #
##############

# Shaman (6)
class Shaman(Hero):
    data = {
        'id': 6,
        'klass': 7, 'hero_power': 6
    }


class 图腾召唤(HeroPower):
    data = {
        'id': 6,
        'klass': 7, 'is_basic': True, 'cost': 2,
    }

    BasicTotems = {"70010", "70011", "70012", "70013"}

    def _candidates(self):
        my_minions = {m.id for m in self.game.get_zone(Zone.Play, self.player_id)}
        return list(self.BasicTotems.difference(my_minions))

    def can_do_action(self, msg_fn=None):
        super_result = super().can_do_action(msg_fn=msg_fn)
        if super_result == self.Inactive:
            return super_result
        # TODO: Require space, and not all 4 totems, which is first?
        if self.game.full(Zone.Play, self.player_id):
            if msg_fn:
                msg_fn('I have too many minions, and I can\'t use it!')
            return self.Inactive
        if not self._candidates():
            if msg_fn:
                msg_fn('I have already own all 4 basic totems!')
            return self.Inactive
        return super_result

    def run(self, target, **kwargs):
        return std_events.pure_summon_events(self.game, choice(self._candidates()), self.player_id, 'last')


# 火舌图腾 (70000) *
Enc_火舌图腾 = ext.create_enchantment({'id': 70000}, *enc_common.apply_fn_add_attack(2), base=AuraEnchantment)


class 火舌图腾(Minion):
    data = {
        'id': 70000,
        'klass': 7, 'cost': 2, 'attack': 0, 'health': 3,
        'race': [Race.Totem],
    }

    class Aura_火舌图腾(Aura):
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
            Enc_火舌图腾.from_card(self.owner, self.game, entity, self)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Aura_火舌图腾(self.game, self)


# 风语者 (70001) *
Enc_风语者 = ext.create_enchantment({'id': 70001}, apply_fn=enc_common.set_target_attr_temp('windfury', True))


class 风语者(Minion):
    data = {
        'id': 70001,
        'klass': 7, 'cost': 4, 'attack': 3, 'health': 3,
        'battlecry': True,
    }

    player_operation_tree = ext.make_conditional_targeted_po_tree(ext.have_friendly_minion)

    check_target = ext.checker_friendly_minion

    def run_battlecry(self, target, **kwargs):
        if target is not None:
            Enc_风语者.from_card(self, self.game, target)
        return []


# 火元素 (70002)
ext.create_damage_minion({
    'id': 70002,
    'klass': 7, 'cost': 6, 'attack': 6, 'health': 5,
    'battlecry': True, 'po_tree': '$HaveTarget',
    'race': [Race.Elemental],
}, 3)


# 先祖治疗 (70003) *

Enc_先祖治疗 = ext.create_enchantment({'id': 70002}, apply_fn=enc_common.set_target_attr_temp('taunt', True))


class 先祖治疗(Spell):
    data = {
        'id': 70003,
        'type': 1, 'klass': 7, 'cost': 0,
        'po_tree': '$HaveTarget',
    }

    can_do_action = ext.require_minion
    check_target = ext.checker_minion

    def run(self, target, **kwargs):
        Enc_先祖治疗.from_card(self, self.game, target)
        return [std_events.Healing(self.game, self, target, target.max_health)]


# 图腾之力 (70004) *
Enc_图腾之力 = ext.create_enchantment({'id': 70003}, *enc_common.apply_fn_add_health(2))


class 图腾之力(Spell):
    data = {
        'id': 70004,
        'type': 1, 'klass': 7, 'cost': 0,
    }

    def run(self, target, **kwargs):
        # Collect all friend totems.
        targets = ext.collect_1p_minions(self, oop=True, player_id=self.player_id)
        targets = [m for m in targets if Race.Totem in m.race]
        for e in targets:
            Enc_图腾之力.from_card(self, self.game, e)
        return []


# 冰霜震击 (70005)
class 冰霜震击(Spell):
    data = {
        'id': 70005,
        'type': 1, 'klass': 7, 'cost': 1,
        'po_tree': '$HaveTarget',
    }
    ext.add_dh_bonus_data(data, 1)

    check_target = ext.checker_enemy_character

    def run(self, target, **kwargs):
        return [std_events.Damage(self.game, self, target, self.dh_values[0]),
                std_events.Freeze(self.game, self, target)]


# 石化武器 (70006) *
class Enc_石化武器(Enchantment):
    data = {
        'id': 70004,
    }

    def __init__(self, game, target, **kwargs):
        super().__init__(game, target, **kwargs)
        std_triggers.DetachOnTurnEnd(self.game, self)

    apply, apply_imm = enc_common.apply_fn_add_attack(2)


class 石化武器(Spell):
    data = {
        'id': 70006,
        'type': 1, 'klass': 7, 'cost': 2,
        'po_tree': '$HaveTarget',
    }

    check_target = ext.checker_friendly_character

    def run(self, target, **kwargs):
        Enc_石化武器.from_card(self, self.game, target)
        return []


# 风怒 (70007) *
Enc_风怒 = ext.create_enchantment({'id': 70005}, apply_fn=enc_common.set_target_attr_temp('windfury', True))


class 风怒(Spell):
    data = {
        'id': 70007,
        'type': 1, 'klass': 7, 'cost': 2,
        'po_tree': '$HaveTarget',
    }

    can_do_action = ext.require_minion
    check_target = ext.checker_minion

    def run(self, target, **kwargs):
        Enc_风怒.from_card(self, self.game, target)
        return []


# 妖术 (70008)
class 妖术(Spell):
    data = {
        'id': 70008,
        'type': 1, 'klass': 7, 'cost': 4,
        'po_tree': '$HaveTarget',
    }

    can_do_action = ext.require_minion
    check_target = ext.checker_minion

    FrogId = 48

    def run(self, target, **kwargs):
        return std_events.replace_events(self.game, target, new_entity=self.FrogId)


# 嗜血 (70009) *
Enc_嗜血 = ext.create_enchantment({'id': 70006}, *enc_common.apply_fn_add_attack(3))


class 嗜血(Spell):
    data = {
        'id': 70009,
        'type': 1, 'klass': 7, 'cost': 5,
    }

    def run(self, target, **kwargs):
        targets = ext.collect_1p_minions(self, oop=True, player_id=self.player_id)
        for e in targets:
            Enc_嗜血.from_card(self, self.game, e)
        return []


# Derivatives

# 石爪图腾 (70010)
ext.blank_minion({
    'id': 70010,
    'rarity': -1, 'klass': 7, 'cost': 1, 'attack': 0, 'health': 2,
    'race': [Race.Totem], 'derivative': True, 'taunt': True,
})


# 治疗图腾 (70011)
class 治疗图腾(Minion):
    data = {
        'id': 70011,
        'rarity': -1, 'klass': 7, 'cost': 1, 'attack': 0, 'health': 2,
        'race': [Race.Totem], 'derivative': True,
    }

    class Trig_治疗图腾(std_triggers.AttachedTrigger):
        respond = [std_events.EndOfTurn]

        def process(self, event: respond[0]):
            if event.player_id != self.owner.player_id:
                return []
            targets = self.game.get_zone(Zone.Play, self.owner.player_id)
            return [std_events.AreaHealing(self.game, self.owner, targets, [1 for _ in targets])]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Trig_治疗图腾(self.game, self)


# 空气之怒图腾 (70012)
ext.blank_minion({
    'id': 70012,
    'rarity': -1, 'klass': 7, 'cost': 1, 'attack': 0, 'health': 2,
    'race': [Race.Totem], 'derivative': True, 'spell_power': 1,
})


# 灼热图腾 (70013)
ext.blank_minion({
    'id': 70013,
    'rarity': -1, 'klass': 7, 'cost': 1, 'attack': 1, 'health': 1,
    'race': [Race.Totem], 'derivative': True,
})
