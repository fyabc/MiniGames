#! /usr/bin/python
# -*- coding: utf-8 -*-

"""Miscellaneous helper functions."""

from collections.abc import Iterable

from ...game.triggers.deathrattle import DrTrigger
from ...utils.game import DHBonusEventType

__author__ = 'fyabc'


def add_dh_bonus_data(data, values, types=DHBonusEventType.Damage):
    """Add damage/healing bonus data of cards.

    See details in the docstring of ``IndependentEntity.description``.

    Example::

        class XXX(Spell):
            '''Deal {5} damage, restore {4} health to your hero.'''
            data = { ... }
            ext.add_dh_bonus_data(data, [5, 4], [DHBonusEventType.Damage, DHBonusEventType.Healing])

            # Other code ...

    :param data:
    :param values:
    :param types:
    :return:
    """
    if not isinstance(values, Iterable):
        values = [values]
    else:
        values = list(values)
    if not isinstance(types, Iterable):
        types = [types for _ in values]
    else:
        types = list(types)
    if len(values) != len(types):
        raise ValueError('Values and types must have same lengths, but got {} vs {}'.format(len(values), len(types)))
    data['dh_values'] = values
    data['dh_types'] = types


__all__ = [
    'add_dh_bonus_data',
]
