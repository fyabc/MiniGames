#! /usr/bin/python
# -*- coding: utf-8 -*-

import sys
from types import new_class

from ...utils.message import warning

__author__ = 'fyabc'


def create_card(data, name, card_type, cls_dict_others=None):
    """Internal function to create a card, called by other creators."""

    assert 'id' in data, 'Data must contain value of key "id".'

    if name is None:
        if 'name' in data:
            name = data['name']
        else:
            name = '{}_{}'.format(card_type.__name__, data['id'])

    cls_dict = {'data': data}

    if cls_dict_others is not None:
        cls_dict.update(cls_dict_others)

    return new_class(name, (card_type,), {}, lambda ns: ns.update(cls_dict))


def add_to_module(result, module_dict):
    """Internal function to add the card to the module dict.

    [NOTE]: This method must be called by other creators directly if `module_dict` is not given.
    """
    if module_dict is None:
        # noinspection PyProtectedMember
        module_dict = sys._getframe(2).f_globals

    # Get the module name of caller.
    result.__module__ = module_dict['__name__']

    if result.__name__ in module_dict:
        warning('Variable {!r} already exists in this module, overwrite it'.format(result.__name__))
    module_dict[result.__name__] = result


__all__ = [
    'create_card',
    'add_to_module',
]
