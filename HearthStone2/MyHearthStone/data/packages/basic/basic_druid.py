#! /usr/bin/python
# -*- coding: utf-8 -*-

from itertools import chain

from MyHearthStone import ext
from MyHearthStone.ext import blank_minion
from MyHearthStone.ext import std_events, std_triggers
from MyHearthStone.ext import enc_common
from MyHearthStone.ext import Spell, Hero, HeroPower, Enchantment
from MyHearthStone.utils.game import order_of_play, Zone, DHBonusEventType

__author__ = 'fyabc'


#############
# Druid (1) #
#############

# Druid (0)
class StdDruid(Hero):
    data = {
        'id': 0,
        'klass': 1, 'hero_power': 0,
    }


class Enc_变形(Enchantment):
    data = {'id': 10000}

    def __init__(self, game, target, **kwargs):
        super().__init__(game, target, **kwargs)
        std_triggers.DetachOnTurnEnd(self.game, self)

    apply, apply_imm = enc_common.apply_fn_add_attack(1)


class 变形(HeroPower):
    data = {
        'id': 0,
        'klass': 1, 'is_basic': True, 'cost': 2,
        'have_target': False,
    }

    def run(self, target, **kwargs):
        hero = self.game.get_hero(self.player_id)
        Enc_变形.from_card(self, self.game, hero)
        return [std_events.GainArmor(self.game, self, hero, 1)]


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
    ext.add_dh_bonus_data(data, 1)

    run = ext.damage_fn(data['dh_values'][0])


# 激活 (10002)
class 激活(Spell):
    data = {
        'id': 10002,
        'type': 1, 'klass': 1, 'cost': 0,
    }

    def run(self, target, **kwargs):
        self.game.add_mana(1, 'T', self.player_id)
        return []


class Enc_爪击(Enchantment):
    data = {'id': 10001}

    def __init__(self, game, target, **kwargs):
        super().__init__(game, target, **kwargs)
        std_triggers.DetachOnTurnEnd(self.game, self)

    apply, apply_imm = enc_common.apply_fn_add_attack(2)


# 爪击 (10003)
class 爪击(Spell):
    data = {
        'id': 10003,
        'type': 1, 'klass': 1, 'cost': 1,
    }

    def run(self, target, **kwargs):
        hero = self.game.get_hero(self.player_id)
        Enc_爪击.from_card(self, self.game, hero)
        return [std_events.GainArmor(self.game, self, hero, 2)]


# 野性印记 (10004)
Enc_野性印记 = ext.create_enchantment(
    {'id': 10002}, *enc_common.apply_fn_add_a_h(2, 2, apply_imm_other=enc_common.set_target_attr('taunt', True)))


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
class 野性成长(Spell):
    data = {
        'id': 10005,
        'type': 1, 'klass': 1, 'cost': 2,
    }

    def run(self, target, **kwargs):
        """Run this spell.

        See <https://hearthstone.gamepedia.com/Wild_Growth#Notes> for more details.

        1. If, after paying this card's Cost, the casting player has 10 available and/or maximum mana,
        this card will generate an Excess Mana card in the player's hand.

        2. Otherwise, it will give an empty Mana Crystal to the casting player.
        """
        player = self.game.get_player(self.player_id)
        if player.displayed_mana() >= player.ManaMax or player.max_mana >= player.ManaMax:
            # TODO: Test the card generation.
            _, status = player.generate(Zone.Hand, 'last', "10010")
            return status['events']
        else:
            player.add_mana(1, 'M')
            return []


# 治疗之触 (10006)
class 治疗之触(Spell):
    data = {
        'id': 10006,
        'type': 1, 'klass': 1, 'cost': 3,
        'have_target': True,
    }
    ext.add_dh_bonus_data(data, 8, DHBonusEventType.Healing)

    def run(self, target, **kwargs):
        return [std_events.Healing(self.game, self, target, self.dh_values[0])]


# 野蛮咆哮 (10007)


# 横扫 (10008)
class 横扫(Spell):
    data = {
        'id': 10008,
        'type': 1, 'klass': 1, 'cost': 4,
        'have_target': True,
    }
    ext.add_dh_bonus_data(data, [4, 1])

    check_target = ext.checker_enemy_character

    def run(self, target, **kwargs):
        """See <https://hearthstone.gamepedia.com/Swipe#Notes> for more details.

        Like most area of effect damaging effect, Swipe deals all its damage before any on-damage
        triggered effects are activated. However, Swipe creates Damage Events in an unusual order:
        first for the targeted character, and then for all other enemy characters in reverse order
        of play; then, all Damage Events are resolved in the same order.
        """
        targets = [target]
        values = [self.dh_values[0]]

        for entity in order_of_play(
                chain(self.game.get_zone(Zone.Play, 1 - self.player_id),
                      self.game.get_zone(Zone.Hero, 1 - self.player_id)), reverse=True):
            if entity is target:
                continue
            targets.append(entity)
            values.append(self.dh_values[1])

        return [std_events.AreaDamage(self.game, self, targets, values)]


# 星火术 (10009)
class 星火术(Spell):
    data = {
        'id': 10009,
        'type': 1, 'klass': 1, 'cost': 6,
        'have_target': True,
    }

    ext.add_dh_bonus_data(data, 5)

    def run(self, target, **kwargs):
        return [std_events.Damage(self.game, self, target, self.dh_values[0]),
                std_events.DrawCard(self.game, self, self.player_id)]


# 法力过剩 (10010)
class 法力过剩(Spell):
    data = {
        'id': 10010,
        'type': 1, 'klass': 1, 'rarity': -1, 'cost': 0,
        'derivative': True,
    }

    run = ext.draw_card_fn(1)
