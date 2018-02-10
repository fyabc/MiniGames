#! /usr/bin/python
# -*- coding: utf-8 -*-

import sys
from functools import partial
from types import new_class

from ..utils.message import warning
from ..game.card import Minion, Weapon

__author__ = 'fyabc'


def create_blank(data, name=None, card_type=Minion, module_dict=None):
    """Create a blank card (without special skills).

    Typical Usage:
        # Give module's global dict.
        # Or called in module's GLOBAL, without `module_dict` param.

    :param data:
    :param name:
    :param card_type:
    :param module_dict: (dict or None)
        The global dict of the module.
        The result card class will be added into this dict automatically.
        NOTE: If not given, will be the global dict of the CALLER.
    :return:
    """

    if module_dict is None:
        # noinspection PyProtectedMember
        module_dict = sys._getframe(1).f_globals

    assert 'id' in data, 'Data must contain value of key "id".'

    if name is None:
        if 'name' in data:
            name = data['name']
        else:
            name = '{}_{}'.format(card_type.__name__, data['id'])

    cls_dict = {'data': data}

    result = new_class(name, (card_type,), {}, lambda ns: ns.update(cls_dict))

    # Get the module name of caller.
    result.__module__ = module_dict['__name__']

    if result.__name__ in module_dict:
        warning('Variable {!r} already exists in this module, overwrite it'.format(result.__name__))
    module_dict[result.__name__] = result
    return result


blank_minion = partial(create_blank, card_type=Minion)
blank_weapon = partial(create_blank, card_type=Weapon)


__all__ = [
    'create_blank',
    'blank_minion',
    'blank_weapon',
]
