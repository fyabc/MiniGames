#! /usr/bin/python
# -*- encoding: utf-8 -*-

"""The module that contains all extension utilities.

Users who want to extend HearthStone should import this module.
"""

from ..game_entities.card import Minion, Spell, Weapon

from ..game_events.basic_events import *
from ..game_events.card_events import *
from ..game_events.attack_events import *
from ..game_events.health_events import *
from ..game_events.random_events import RandomTargetDamage
from ..game_events.game_event import *
from ..game_events.play_events import *
from ..game_events.death_events import *

from ..game_handlers.game_handler import *
from ..game_handlers.basic_handlers import *
from ..game_handlers.damage_handlers import *
from ..game_handlers.card_handlers import *

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
