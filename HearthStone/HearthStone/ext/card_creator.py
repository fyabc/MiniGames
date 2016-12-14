#! /usr/bin/python
# -*- coding: utf-8 -*-

"""Some helper functions to create cards."""

import sys
from types import new_class

from .ext import *
from .card_filters import *

__author__ = 'fyabc'


# Minion creators.
# m_xxx, m represents Minion.

def m_blank(name, data):
    cls_dict = {'_data': data}

    result = new_class(name, (Minion,), {}, lambda ns: ns.update(cls_dict))

    # Get the module name of caller.
    result.__module__ = sys._getframe(1).f_globals['__name__']
    return result


def m_bc_summon(name, data, relative_location=+1, **kwargs):
    random_summon = False
    card_id = kwargs.pop('card_id', None)

    if card_id is None:
        random_summon = True
        conditions = kwargs.pop('conditions', [])

    def run_battle_cry(self, player_id, index):
        self.game.add_event_quick(
            AddMinionToDesk,
            card_id if not random_summon else random_card(*conditions),
            index + relative_location,
            player_id,
        )

    cls_dict = {'_data': data, 'run_battle_cry': run_battle_cry}

    result = new_class(name, (Minion,), {}, lambda ns: ns.update(cls_dict))

    # Get the module name of caller.
    result.__module__ = sys._getframe(1).f_globals['__name__']
    return result


__all__ = [
    'm_blank',
]
