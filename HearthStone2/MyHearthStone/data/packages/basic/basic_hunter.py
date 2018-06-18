#! /usr/bin/python
# -*- coding: utf-8 -*-

# TODO: Apply DH values.

import random

from MyHearthStone import ext
from MyHearthStone.ext import enc_common
from MyHearthStone.ext import std_events, std_triggers
from MyHearthStone.ext import Minion, Spell, Hero, HeroPower
from MyHearthStone.utils.game import Zone, Race

__author__ = 'fyabc'


##############
# Hunter (2) #
##############

# Hunter (1)
class StdHunter(Hero):
    data = {
        'id': 1,
        'klass': 2, 'hero_power': 1,
    }


class 稳固射击(HeroPower):
    data = {
        'id': 1,
        'klass': 2, 'is_basic': True, 'cost': 2,
        'have_target': False,
    }
    ext.add_dh_bonus_data(data, [2])

    def run(self, target, **kwargs):
        return [std_events.Damage(
            self.game, self,
            target=self.game.get_hero(1 - self.player_id),
            value=self.dh_values[0])]


# 森林狼 (20000)
class 森林狼(Minion):
    data = {
        'id': 20000,
        'klass': 2, 'cost': 1, 'attack': 1, 'health': 1,
        'race': [Race.Beast],
    }

    # TODO


# 驯兽师 (20001)
Enc_驯兽师 = ext.create_enchantment(
    {'id': 20001}, *enc_common.apply_fn_add_a_h(2, 2, apply_imm_other=enc_common.set_target_attr('taunt', True)))


class 驯兽师(Minion):
    data = {
        'id': 20001,
        'klass': 2, 'cost': 4, 'attack': 4, 'health': 3,
        'battlecry': True,
    }

    have_target = property(fget=ext.make_have_friendly_race(Race.Beast))

    def check_target(self, target):
        if not ext.checker_friendly_minion(self, target):
            return False
        assert isinstance(target, Minion)
        if Race.Beast not in target.race:
            return False
        return True

    def run_battlecry(self, target, **kwargs):
        if target is not None:
            Enc_驯兽师.from_card(self, self.game, target)
        return []

# 苔原犀牛 (20002)


# 饥饿的秃鹫 (20003)
class 饥饿的秃鹫(Minion):
    data = {
        'id': 20003,
        'klass': 2, 'cost': 5, 'attack': 3, 'health': 2,
        'race': [Race.Beast],
    }

    class Trig_饥饿的秃鹫(std_triggers.Trigger):
        respond = [std_events.Summon]

        def process(self, event: respond[0]):
            minion = event.minion
            if minion == self.owner:
                return []
            if minion.zone == Zone.Play and minion.player_id == self.owner.player_id and Race.Beast in minion.race:
                return [std_events.DrawCard(self.game, self.owner, self.owner.player_id)]
            return []

    def __init__(self, game, player_id):
        super().__init__(game, player_id)
        self.Trig_饥饿的秃鹫(self.game, self)


# 猎人印记 (20004)
Enc_猎人印记 = ext.create_enchantment({'id': 20003}, *enc_common.apply_fn_set_health(1))


class 猎人印记(Spell):
    data = {
        'id': 20004,
        'type': 1, 'klass': 2, 'cost': 1,
        'have_target': True,
    }

    check_target = ext.checker_minion

    def run(self, target, **kwargs):
        Enc_猎人印记.from_card(self, self.game, target)
        return []


# 奥术射击 (20005)
class 奥术射击(Spell):
    data = {
        'id': 20005,
        'type': 1, 'klass': 2, 'cost': 1,
        'have_target': True,
    }
    ext.add_dh_bonus_data(data, 2)

    run = ext.damage_fn(data.get('dh_values', [])[0])


# 追踪术 (20006)
class 追踪术(Spell):
    data = {
        'id': 20006,
        'type': 1, 'klass': 2, 'cost': 1,
    }

    # TODO


# 动物伙伴 (20007)
class 动物伙伴(Spell):
    data = {
        'id': 20007,
        'type': 1, 'klass': 2, 'cost': 3,
    }

    can_do_action = ext.require_board_not_full

    def run(self, target, **kwargs):
        summon_id = random.choice(["20010", "20011", "20012"])
        return std_events.pure_summon_events(self.game, summon_id, self.player_id, 'last')


# 杀戮命令 (20008)
class 杀戮命令(Spell):
    data = {
        'id': 20008,
        'type': 1, 'klass': 2, 'cost': 3,
        'have_target': True,
    }
    ext.add_dh_bonus_data(data, [3, 5])

    def can_do_action(self, msg_fn=None):
        super_result = super().can_do_action(msg_fn=msg_fn)
        if super_result == self.Inactive:
            return super_result

        if self.zone == Zone.Hand and ext.have_friendly_beast(self):
            return self.Highlighted
        return super_result

    def run(self, target, **kwargs):
        value = self.dh_values[1] if ext.have_friendly_beast(self) else self.dh_values[0]
        return [std_events.Damage(self.game, self, target, value)]


# 多重射击 (20009)
class 多重射击(Spell):
    data = {
        'id': 20009,
        'type': 1, 'klass': 2, 'cost': 4,
    }
    ext.add_dh_bonus_data(data, 3)

    def can_do_action(self, msg_fn=None):
        super_result = super().can_do_action(msg_fn=msg_fn)

        if self.zone == Zone.Hand and len(self.game.get_zone(Zone.Play, 1 - self.player_id)) < 2:
            if msg_fn:
                msg_fn('Your opponent must have at least 2 minions!')
            return self.Inactive

        return super_result

    def run(self, target, **kwargs):
        """Deal damage in random order.

        See <https://hearthstone.gamepedia.com/Damage#Advanced_rules> and its explanation on "Multi-Shot" for details.
        """
        zone = self.game.get_zone(Zone.Play, 1 - self.player_id)
        if len(zone) == 0:
            return []
        elif len(zone) < 2:
            real_targets = zone
        else:
            real_targets = random.sample(zone, 2)
        return [std_events.AreaDamage(self.game, self, real_targets, [self.dh_values[0] for _ in real_targets])]


# Derivations.

# 米莎 (20010)
ext.blank_minion({
    'id': 20010,
    'rarity': -1, 'klass': 2, 'cost': 3, 'attack': 4, 'health': 4,
    'race': [Race.Beast], 'derivative': True, 'taunt': True,
})


# 雷欧克 (20011)
class 雷欧克(Minion):
    data = {
        'id': 20011,
        'rarity': -1, 'klass': 2, 'cost': 3, 'attack': 2, 'health': 4,
        'race': [Race.Beast], 'derivative': True,
    }

    # TODO


# 霍弗 (20012)
ext.blank_minion({
    'id': 20012,
    'rarity': -1, 'klass': 2, 'cost': 3, 'attack': 4, 'health': 2,
    'race': [Race.Beast], 'derivative': True, 'charge': True,
})
