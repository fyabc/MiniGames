#! /usr/bin/python
# -*- coding: utf-8 -*-

from .game_entity import GameEntity, SetDataMeta

__author__ = 'fyabc'


class Card(GameEntity, metaclass=SetDataMeta):
    """[NO_DESCRIPTION]"""

    _data = {
        'id': None,
        'type': 0,
        'name': '',
        'package': 0,
        'rarity': 0,
        'klass': 0,
        'race': [],
        'CAH': [0, 1, 1],
        'overload': 0,
        'spell_power': 0,
        'description': '',
    }


class Minion(Card):
    pass


class Spell(Card):
    pass


class Weapon(Card):
    pass


class HeroCard(Card):
    pass
