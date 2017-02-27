#! /usr/bin/python
# -*- encoding: utf-8 -*-

"""The core of the ext package."""

from ..game_entities.card import Minion, Spell, Weapon

from ..game_events import *

from ..game_handlers.base import *
from ..game_handlers.basic import *
from ..game_handlers.damage import *
from ..game_handlers.card import *

__author__ = 'fyabc'


def set_description(card_table):
    for card, description in card_table.items():
        card._data['description'] = description


def desk_location(game, minion):
    for player_id in (0, 1):
        for i, m in game.players[player_id].desk:
            if m == minion:
                return player_id, i
    return None, None
