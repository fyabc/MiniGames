#! /usr/bin/python
# -*- coding: utf-8 -*-

"""Enchantment creators."""

from types import new_class as _new_class

from .utils import add_to_module as _add_to_module
from ...game.enchantments.enchantment import Enchantment, AuraEnchantment
from ...game.enchantments.aura import Aura
from ...game.enchantments import common as enc_common
from ...game.enchantments.dh_bonus import *
from ...game.enchantments.deathrattle import *

__author__ = 'fyabc'


def create_enchantment(data, apply_fn, apply_imm_fn=None, base=Enchantment,
                       name=None, module_dict=None, add_to_module=False):
    assert 'id' in data, 'Data must contain value of key "id".'

    if apply_imm_fn is None:
        def apply_imm_fn(self):
            pass

    if name is None:
        if 'name' in data:
            name = data['name']
        else:
            name = '{}_{}'.format(Enchantment.__name__, data['id'])

    cls_dict = {'data': data, 'apply': apply_fn, 'apply_imm': apply_imm_fn}

    cls = _new_class(name, (base,), {}, lambda ns: ns.update(cls_dict))
    if add_to_module:
        _add_to_module(cls, module_dict)

    return cls
