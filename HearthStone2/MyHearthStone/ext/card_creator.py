#! /usr/bin/python
# -*- coding: utf-8 -*-

import sys
from functools import partial
from types import new_class

from ..game.card import Minion, Weapon

__author__ = 'fyabc'


def gen_basic_description(data):
    """Generate basic description for blank cards."""

    descriptions = []

    if data.get('taunt') is True:
        descriptions.append('嘲讽')

    if data.get('charge') is True:
        descriptions.append('冲锋')

    if data.get('divine_shield') is True:
        descriptions.append('圣盾')

    if data.get('windfury') is True:
        descriptions.append('风怒')

    if data.get('stealth') is True:
        descriptions.append('潜行')

    if data.get('poisonous') is True:
        descriptions.append('剧毒')

    if data.get('lifesteal') is True:
        descriptions.append('吸血')

    spell_power = data.get('spell_power', 0)
    if spell_power != 0:
        descriptions.append('法术伤害{}{}'.format('+' if spell_power > 0 else '', spell_power))

    return '，'.join(descriptions)


def create_blank(data, name=None, card_type=Minion):
    if name is None:
        name = data['name']

    if 'description' not in data:
        data['description'] = gen_basic_description(data)

    cls_dict = {'_data': data}

    result = new_class(name, (card_type,), {}, lambda ns: ns.update(cls_dict))

    # Get the module name of caller.
    result.__module__ = sys._getframe(1).f_globals['__name__']
    return result


blank_minion = partial(create_blank, card_type=Minion)
blank_weapon = partial(create_blank, card_type=Weapon)


__all__ = [
    'gen_basic_description',
    'create_blank',
    'blank_minion',
    'blank_weapon',
]
