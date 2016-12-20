#! /usr/bin/python
# -*- coding: utf-8 -*-

"""Some helper functions to create cards."""

import sys
from types import new_class

from .ext import *
from .card_filters import *
from ..constants import card_constants as cc

__author__ = 'fyabc'


# Minion creators.
# m_xxx, m represents Minion.

def m_blank(name, data):
    cls_dict = {'_data': data}

    result = new_class(name, (Minion,), {}, lambda ns: ns.update(cls_dict))

    # Get the module name of caller.
    result.__module__ = sys._getframe(1).f_globals['__name__']
    return result


def m_summon(name, data, bc_or_dr=True, **kwargs):
    random_summon = False
    card_id = kwargs.pop('card_id', None)

    if card_id is None:
        random_summon = True
        conditions = kwargs.pop('conditions', [])

    relative_location = kwargs.pop('relative_location', +1 if bc_or_dr else 0)

    def summon(self, player_id, index):
        self.game.add_event_quick(
            AddMinionToDesk,
            card_id if not random_summon else random_card(*conditions),
            index + relative_location,
            player_id,
        )

    cls_dict = {'_data': data, 'run_battle_cry' if bc_or_dr else 'run_death_rattle': summon}

    result = new_class(name, (Minion,), {}, lambda ns: ns.update(cls_dict))

    # Get the module name of caller.
    result.__module__ = sys._getframe(1).f_globals['__name__']
    return result


# Common target validators.
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


__all__ = [
    'm_blank',
    'm_summon',
    'validator_minion',
    'validator_enemy_minion',
]
