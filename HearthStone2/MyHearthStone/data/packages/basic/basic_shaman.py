#! /usr/bin/python
# -*- coding: utf-8 -*-

from random import choice

from MyHearthStone import ext
from MyHearthStone.ext import Minion, Spell, Hero, HeroPower
from MyHearthStone.ext import std_events
from MyHearthStone.ext import std_triggers
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


# 火舌图腾 (70000)

# 风语者 (70001)

# 火元素 (70002)


# 先祖治疗 (70003)
class 先祖治疗(Spell):
    data = {
        'id': 70003,
        'type': 1, 'klass': 7, 'cost': 0,
        'po_tree': '$HaveTarget',
    }

    can_do_action = ext.require_minion
    check_target = ext.checker_minion

    def run(self, target, **kwargs):
        # TODO
        return []

# 图腾之力 (70004)


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
        # TODO
        return []


# 石化武器 (70006)
class 石化武器(Spell):
    data = {
        'id': 70006,
        'type': 1, 'klass': 7, 'cost': 2,
        'po_tree': '$HaveTarget',
    }

    check_target = ext.checker_friendly_character

    def run(self, target, **kwargs):
        # TODO
        return []


# 风怒 (70007)
class 风怒(Spell):
    data = {
        'id': 70007,
        'type': 1, 'klass': 7, 'cost': 2,
        'po_tree': '$HaveTarget',
    }

    can_do_action = ext.require_minion
    check_target = ext.checker_minion

    def run(self, target, **kwargs):
        # TODO
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

    def run(self, target, **kwargs):
        # TODO
        return []

# 嗜血 (70009)


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
