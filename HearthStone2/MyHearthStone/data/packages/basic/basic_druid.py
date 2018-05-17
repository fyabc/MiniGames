#! /usr/bin/python
# -*- coding: utf-8 -*-

from itertools import chain

from MyHearthStone import ext
from MyHearthStone.ext import blank_minion
from MyHearthStone.ext import std_events
from MyHearthStone.ext import enc_common
from MyHearthStone.ext import Spell
from MyHearthStone.utils.game import order_of_play, Zone

__author__ = 'fyabc'


#############
# Druid (1) #
#############

# 埃隆巴克保护者 (10000)
blank_minion({
    'id': 10000,
    'klass': 1, 'cost': 8, 'attack': 8, 'health': 8,
    'taunt': True,
})


# 月火术 (10001)
class 月火术(Spell):
    data = {
        'id': 10001,
        'type': 1, 'klass': 1, 'cost': 0,
        'have_target': True,
    }

    run = ext.damage_fn(1)


# 激活 (10002)
class 激活(Spell):
    data = {
        'id': 10002,
        'type': 1, 'klass': 1, 'cost': 0,
    }

    def run(self, target, **kwargs):
        self.game.add_mana(1, 'T', self.player_id)
        return []


# 爪击 (10003)


# 野性印记 (10004)
Enc_野性印记 = ext.create_enchantment(
    {'id': 10000}, *enc_common.apply_fn_add_a_h(2, 2, apply_other=enc_common.set_target_attr('taunt', True)))


class 野性印记(Spell):
    data = {
        'id': 10004,
        'type': 1, 'klass': 1, 'cost': 2,
        'have_target': True,
    }

    check_target = ext.checker_minion

    def run(self, target, **kwargs):
        Enc_野性印记.from_card(self, self.game, target)
        return []

# 野性成长 (10005)


# 治疗之触 (10006)
class 治疗之触(Spell):
    data = {
        'id': 10006,
        'type': 1, 'klass': 1, 'cost': 3,
        'have_target': True,
    }

    def run(self, target, **kwargs):
        return [std_events.Healing(self.game, self, target, 8)]


# 野蛮咆哮 (10007)


# 横扫 (10008)
class 横扫(Spell):
    data = {
        'id': 10008,
        'type': 1, 'klass': 1, 'cost': 4,
        'have_target': True,
    }

    check_target = ext.checker_enemy_character

    def run(self, target, **kwargs):
        """See <https://hearthstone.gamepedia.com/Swipe#Notes> for more details.

        Like most area of effect damaging effect, Swipe deals all its damage before any on-damage
        triggered effects are activated. However, Swipe creates Damage Events in an unusual order:
        first for the targeted character, and then for all other enemy characters in reverse order
        of play; then, all Damage Events are resolved in the same order.
        """
        targets = [target]
        values = [4]

        for entity in order_of_play(
                chain(self.game.get_zone(Zone.Play, 1 - self.player_id),
                      self.game.get_zone(Zone.Hero, 1 - self.player_id)), reverse=True):
            if entity == target:
                continue
            targets.append(entity)
            values.append(1)

        return [std_events.AreaDamage(self.game, self, targets, values)]


# 星火术 (10009)
class 星火术(Spell):
    data = {
        'id': 10009,
        'type': 1, 'klass': 1, 'cost': 6,
        'have_target': True,
    }

    def run(self, target, **kwargs):
        return [std_events.DrawCard(self.game, self, self.player_id), std_events.Damage(self.game, self, target, 5)]
