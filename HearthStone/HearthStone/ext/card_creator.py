#! /usr/bin/python
# -*- coding: utf-8 -*-

"""Some helper functions to create cards."""

import sys
from types import new_class
from functools import partial

from .ext import *
from .card_filters import *
from ..constants import card_constants as cc

__author__ = 'fyabc'


def gen_basic_description(data):
    """Generate basic description for blank cards."""

    descriptions = []

    attack_number = data.get('attack_number')
    if attack_number is not None:
        if attack_number == 0:
            descriptions.append('无法攻击')
        elif attack_number == 2:
            descriptions.append('风怒')
        elif attack_number == 4:
            descriptions.append('超级风怒')

    if data.get('charge') is True:
        descriptions.append('冲锋')

    if data.get('divine_shield') is True:
        descriptions.append('圣盾')

    if data.get('taunt') is True:
        descriptions.append('嘲讽')

    spell_power = data.get('spell_power')
    if spell_power is not None and spell_power != 0:
        descriptions.append('法术伤害{}{}'.format('+' if spell_power > 0 else '', spell_power))

    return '，'.join(descriptions)


def create_blank(name, data, card_type=Minion):
    if 'description' not in data:
        data['description'] = gen_basic_description(data)

    cls_dict = {'_data': data}

    result = new_class(name, (card_type,), {}, lambda ns: ns.update(cls_dict))

    # Get the module name of caller.
    result.__module__ = sys._getframe(1).f_globals['__name__']
    return result


m_blank = partial(create_blank, card_type=Minion)
w_blank = partial(create_blank, card_type=Weapon)


def m_summon(name, data, bc_or_dr=True, **kwargs):
    """

    :param name:
    :param data:
    :param bc_or_dr: bool
        If True, summon on battle cry, else summon on death rattle.
    :param kwargs: Other keyword arguments.
        conditions: list of string
            Condition must be a SQL condition expression.
    :return: Minion class.
    """

    random_summon = False
    card_id = kwargs.pop('card_id', None)

    if card_id is None:
        random_summon = True
        conditions = kwargs.pop('conditions', [])

    relative_location = kwargs.pop('relative_location', +1 if bc_or_dr else 0)

    cls_dict = {'_data': data}

    if bc_or_dr:
        def run_battle_cry(self, player_id, index, target=None):
            self.game.add_event_quick(
                AddMinionToDesk,
                card_id if not random_summon else random_card(*conditions),
                index + relative_location,
                player_id,
            )

        cls_dict['run_battle_cry'] = run_battle_cry
    else:
        def run_death_rattle(self, player_id, index):
            self.game.add_event_quick(
                AddMinionToDesk,
                card_id if not random_summon else random_card(*conditions),
                index + relative_location,
                player_id,
            )

        cls_dict['run_death_rattle'] = run_death_rattle

    result = new_class(name, (Minion,), {}, lambda ns: ns.update(cls_dict))

    # Get the module name of caller.
    result.__module__ = sys._getframe(1).f_globals['__name__']
    return result


# Common target validators.
def validator_enemy(self, target):
    result = super(self.__class__, self).validate_target(target)
    if result is not True:
        return result

    if target.player_id == self.player_id:
        return 'Must choose an enemy minion!'

    return True


def validator_minion(self, target):
    result = super(self.__class__, self).validate_target(target)
    if result is not True:
        return result

    if target.type != cc.Type_minion:
        return 'The target must be a minion!'

    return True


def validator_enemy_minion(self, target):
    result = super(self.__class__, self).validate_target(target)
    if result is not True:
        return result

    if target.type != cc.Type_minion:
        return 'The target must be a minion!'

    if target.player_id == self.player_id:
        return 'Must choose an enemy minion!'

    return True


# Common spell actions.
def action_damage(value):
    def action(self, player_id, target):
        self.game.add_event_quick(SpellDamage, self, target, value)
    return action


def action_destroy(self, player_id, target):
    self.game.add_event_quick(MinionDeath, target)


__all__ = [
    'create_blank',
    'm_blank',
    'w_blank',
    'm_summon',

    'validator_enemy',
    'validator_minion',
    'validator_enemy_minion',

    'action_damage',
    'action_destroy',
]
