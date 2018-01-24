#! /usr/bin/python
# -*- coding: utf-8 -*-

import sys
from functools import partial
from types import new_class

from ..game.card import Minion, Weapon

__author__ = 'fyabc'


def create_blank(data, name=None, card_type=Minion):
    assert 'id' in data, 'Data must contain value of key "id".'

    if name is None:
        if 'name' in data:
            name = data['name']
        else:
            name = '{}_{}'.format(card_type.__name__, data['id'])

    cls_dict = {'_data': data}

    result = new_class(name, (card_type,), {}, lambda ns: ns.update(cls_dict))

    # Get the module name of caller.
    result.__module__ = sys._getframe(1).f_globals['__name__']
    return result


blank_minion = partial(create_blank, card_type=Minion)
blank_weapon = partial(create_blank, card_type=Weapon)


__all__ = [
    'create_blank',
    'blank_minion',
    'blank_weapon',
]
