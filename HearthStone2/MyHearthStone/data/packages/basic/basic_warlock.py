#! /usr/bin/python
# -*- coding: utf-8 -*-

from random import choice

from MyHearthStone import ext
from MyHearthStone.ext import Minion, Spell, Hero, HeroPower
from MyHearthStone.ext import std_events
from MyHearthStone.utils.game import Race, Zone, DHBonusEventType

__author__ = 'fyabc'


###############
# Warlock (8) #
###############

# Warlock (7)
class Warlock(Hero):
    data = {
        'id': 7,
        'klass': 8, 'hero_power': 7,
    }


class 生命分流(HeroPower):
    data = {
        'id': 7,
        'klass': 8, 'is_basic': True, 'cost': 2,
    }
    ext.add_dh_bonus_data(data, 2)

    def run(self, target, **kwargs):
        return [std_events.Damage(self.game, self, target=self.game.get_hero(self.player_id), value=self.dh_values[0]),
                std_events.DrawCard(self.game, self, self.player_id)]


# 虚空行者 (80000)
ext.blank_minion({
    'id': 80000,
    'klass': 8, 'cost': 1, 'attack': 1, 'health': 3,
    'taunt': True, 'race': [Race.Demon],
})


# 魅魔 (80001)
class 魅魔(Minion):
    data = {
        'id': 80001,
        'klass': 8, 'cost': 2, 'attack': 4, 'health': 3,
        'battlecry': True, 'race': [Race.Demon],
    }

    def run_battlecry(self, target, **kwargs):
        target = choice(self.game.get_zone(Zone.Hand, self.player_id))
        return [std_events.DiscardCard(self.game, self, target)]


# 恐惧地狱火 (80002)
class 恐惧地狱火(Minion):
    data = {
        'id': 80002,
        'klass': 8, 'cost': 6, 'attack': 6, 'health': 6,
        'battlecry': True, 'race': [Race.Demon],
    }

    def run_battlecry(self, target, **kwargs):
        targets = ext.collect_all(self, oop=True, except_list=(self,))
        return [std_events.AreaDamage(self.game, self, targets, [1 for _ in targets])]


# 牺牲契约 (80003)
class 牺牲契约(Spell):
    data = {
        'id': 80003,
        'type': 1, 'klass': 8, 'cost': 0,
        'po_tree': '$HaveTarget',
    }
    ext.add_dh_bonus_data(data, 5, DHBonusEventType.Healing)

    # TODO: Can do action and check target: have demon.

    def can_do_action(self, msg_fn=None):
        super_result = super().can_do_action(msg_fn)
        if super_result == self.Inactive:
            return super_result
        if any(Race.Demon in e.race for e in ext.collect_all(self, oop=False)):
            return self.Active
        else:
            if msg_fn:
                msg_fn('No valid target, I can\'t use it!')
            return self.Inactive

    def check_target(self, target, **kwargs):
        if not super().check_target(target, **kwargs):
            return False
        if Race.Demon not in target.race:
            return False
        return True

    def run(self, target, **kwargs):
        target.to_be_destroyed = True
        return [std_events.Healing(self.game, self, self.game.get_hero(self.player_id), self.dh_values[0])]


# 灵魂之火 (80004)
class 灵魂之火(Spell):
    data = {
        'id': 80004,
        'type': 1, 'klass': 8, 'cost': 1,
        'po_tree': '$HaveTarget',
    }
    ext.add_dh_bonus_data(data, 4)

    def run(self, target, **kwargs):
        discard_target = choice(self.game.get_zone(Zone.Hand, self.player_id))
        return [std_events.Damage(self.game, self, target, self.dh_values[0]),
                std_events.DiscardCard(self.game, self, discard_target)]


# 死亡缠绕 (80005)
class 死亡缠绕(Spell):
    """[NOTE]: This is a classic card of two-step effect and conditional effect."""
    data = {
        'id': 80005,
        'type': 1, 'klass': 8, 'cost': 1,
        'po_tree': '$HaveTarget',
    }
    ext.add_dh_bonus_data(data, 1)

    can_do_action = ext.require_minion
    check_target = ext.checker_minion

    def run(self, target, **kwargs):
        # [NOTE]: The default parameter (event self) of condition is ignored.
        def condition(_):
            return not target.alive
        return [
            std_events.Damage(self.game, self, target, self.dh_values[0]),
            std_events.condition_wrap(std_events.DrawCard(self.game, self), condition),
        ]

# 腐蚀术 (80006) *


# 吸取生命 (80007)
class 吸取生命(Spell):
    data = {
        'id': 80007,
        'type': 1, 'klass': 8, 'cost': 3,
        'po_tree': '$HaveTarget',
    }
    ext.add_dh_bonus_data(data, [2, 2], [DHBonusEventType.Damage, DHBonusEventType.Healing])

    def run(self, target, **kwargs):
        return [
            std_events.Damage(self.game, self, target, self.dh_values[0]),
            std_events.Healing(self.game, self, target, self.dh_values[1]),
        ]


# 暗影箭 (80008)
class 暗影箭(Spell):
    data = {
        'id': 80008,
        'type': 1, 'klass': 8, 'cost': 3,
        'po_tree': '$HaveTarget',
    }
    ext.add_dh_bonus_data(data, 4)

    can_do_action = ext.require_minion
    check_target = ext.checker_minion

    def run(self, target, **kwargs):
        return [std_events.Damage(self.game, self, target, self.dh_values[0])]


# 地狱烈焰 (80009)
class 地狱烈焰(Spell):
    data = {
        'id': 80009,
        'type': 1, 'klass': 8, 'cost': 4,
    }
    ext.add_dh_bonus_data(data, 3)

    def run(self, target, **kwargs):
        targets = ext.collect_all(self, oop=True)
        return [std_events.AreaDamage(self.game, self, targets, [self.dh_values[0] for _ in targets])]
