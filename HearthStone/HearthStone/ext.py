#! /usr/bin/python
# -*- encoding: utf-8 -*-

"""The module that contains all extension utilities.

Users who want to extend HearthStone should import this module.
"""

from .game_entities.card import Minion, Spell, Weapon

__author__ = 'fyabc'


def set_description(card_table):
    for card, description in card_table.items():
        card._data['description'] = description


__all__ = [
    'Minion',
    'Spell',
    'Weapon',
]
