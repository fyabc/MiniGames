#! /usr/bin/python
# -*- encoding: utf-8 -*-

"""The module that contains all extension utilities.

Users who want to extend HearthStone should import this module.


Docstring for users
===================

    How to create your own card
    ---------------------------
    If you want to create your own card, you need to make a new class of your card.
    The new class must be subclass of `Minion`, `Spell` or `Weapon` (in `HearthStone.game_entities.card` package)

    Assume that the new card is a minion `Minion001`, package is `package001`.

    1. Create a directory of your own extension with any name you like, such as "my_HS_extension".
        Tips:
            The default data path is "~/data/", "~" is the root of the HearthStone package.
            The default user data path is "~/userdata/HearthStoneCard/".
            You can also add your own card data path by add it into `HearthStone.utils.path_utils.LoadDataPath`.

        NOTE: Names of subdirectories are fixed.
            Cards must be in "HearthStoneCard" directory.
            Heroes must be in "HearthStoneHero" directory.
            These names are defined in `HearthStone.utils.path_utils.CardPackageName`, etc.

    2. Create a package file
        Create a Python script into the user card data path.

        It is recommended that the file name is same as the package name, so you should create a file `package001.py`.

        Your extension directory is like this:
        my_HS_extension/
            HearthStoneCard/
                package001.py
            HearthStoneHero/      (This directory can be omitted now)

    3. Set package information
        (This is unnecessarily now, need more doc)

    4. Create a card
        [todo]
"""

from ..game_entities.card import Minion, Spell, Weapon

from ..game_events.basic_events import *
from ..game_events.card_events import *
from ..game_events.attack_events import *
from ..game_events.health_events import *
from ..game_events.real_time_events import *
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
