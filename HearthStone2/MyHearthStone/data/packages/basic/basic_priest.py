#! /usr/bin/python
# -*- coding: utf-8 -*-

from itertools import chain

from MyHearthStone import ext
from MyHearthStone.ext import Minion, Spell, Hero, HeroPower
from MyHearthStone.ext import std_events, std_triggers
from MyHearthStone.utils.game import Zone, Type

__author__ = 'fyabc'


##############
# Priest (5) #
##############

# Priest (4)
class Priest(Hero):
    data = {
        'id': 4,
        'klass': 5, 'hero_power': 4,
    }


class 次级治疗术(HeroPower):
    data = {
        'id': 4,
        'klass': 5, 'is_basic': True, 'cost': 2,
        'po_tree': '$HaveTarget',
    }
    ext.add_dh_bonus_data(data, 2)

    def run(self, target, **kwargs):
        return [std_events.Healing(self.game, self, target, self.dh_values[0])]


# 北郡牧师 (50000)
class 北郡牧师(Minion):
    # TODO: Need test.

    data = {
        'id': 50000,
        'klass': 5, 'cost': 1, 'attack': 1, 'health': 3,
    }

    class Trig_北郡牧师(std_triggers.AttachedTrigger):
        respond = [std_events.Healing]

        def process(self, event: respond[0]):
            if event.target.type != Type.Minion:
                return []
            return [std_events.DrawCard(self.game, self.owner, self.owner.player_id)]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Trig_北郡牧师(self.game, self)


# 神圣惩击 (50001)
class 神圣惩击(Spell):
    data = {
        'id': 50001,
        'type': 1, 'klass': 5, 'cost': 1,
        'po_tree': '$HaveTarget',
    }
    ext.add_dh_bonus_data(data, 2)

    def run(self, target, **kwargs):
        return [std_events.Damage(self.game, self, target, self.dh_values[0])]


# 心灵视界 (50002)
class 心灵视界(Spell):
    """[NOTE]: This is a classic card of (permanent) copy effect."""
    data = {
        'id': 50002,
        'type': 1, 'klass': 5, 'cost': 1,
    }

    def run(self, target, **kwargs):
        self.game.generate()
        return []


# 真言术：盾 (50003)
class 真言术_盾(Spell):
    data = {
        'id': 50003,
        'type': 1, 'klass': 5, 'cost': 1,
        'po_tree': '$HaveTarget',
    }

    can_do_action = ext.require_minion
    check_target = ext.checker_minion

    def run(self, target, **kwargs):
        # TODO
        return []


# 神圣之灵 (50004)
class 神圣之灵(Spell):
    data = {
        'id': 50005,
        'type': 1, 'klass': 5, 'cost': 2,
        'po_tree': '$HaveTarget',
    }

    can_do_action = ext.require_minion
    check_target = ext.checker_minion

    def run(self, target, **kwargs):
        # TODO
        return []


# 心灵震爆 (50005)
class 心灵震爆(Spell):
    data = {
        'id': 50005,
        'type': 1, 'klass': 5, 'cost': 2,
    }
    ext.add_dh_bonus_data(data, 5)

    def run(self, target, **kwargs):
        return [std_events.Damage(self.game, self, self.game.get_hero(1 - self.player_id), self.dh_values[0])]


# 暗言术：痛 (50006)
class 暗言术_痛(Spell):
    data = {
        'id': 50006,
        'type': 1, 'klass': 5, 'cost': 2,
        'po_tree': '$HaveTarget',
    }

    can_do_action, check_target = ext.action_target_checker_factory_cond_minion(lambda target: target.attack <= 3)

    def run(self, target, **kwargs):
        target.to_be_destroyed = True
        return []


# 暗言术：灭 (50007)
class 暗言术_灭(Spell):
    data = {
        'id': 50006,
        'type': 1, 'klass': 5, 'cost': 3,
        'po_tree': '$HaveTarget',
    }

    can_do_action, check_target = ext.action_target_checker_factory_cond_minion(lambda target: target.attack >= 5)

    def run(self, target, **kwargs):
        target.to_be_destroyed = True
        return []

# 神圣新星 (50008)


# 精神控制 (50009)
class 精神控制(Spell):
    """[NOTE]: This is a classic card of (permanent) mind control effect."""
    data = {
        'id': 50009,
        'type': 1, 'klass': 5, 'cost': 10,
        'po_tree': '$HaveTarget',
    }

    # TODO: Extract these condition-message pairs.
    can_do_action = ext.action_checker_factory_cond(
        (ext.have_enemy_minion, 'No enemy minions in play, and I can\'t use it!'),
        (lambda self: not self.game.full(Zone.Play, self.player_id), 'I have too many minions, and I can\'t use it!'),
    )
    check_target = ext.checker_enemy_minion

    def run(self, target, **kwargs):
        entity, status = self.game.move(target.player_id, target.zone, target, self.player_id, Zone.Play, 'last')
        return status['events']
