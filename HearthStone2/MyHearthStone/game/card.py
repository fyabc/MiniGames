#! /usr/bin/python
# -*- coding: utf-8 -*-

from .game_entity import GameEntity, SetDataMeta

__author__ = 'fyabc'


class Card(GameEntity, metaclass=SetDataMeta):
    """[NO_DESCRIPTION]

    The class of card.
    """

    # Locations of the card.
    NULL = 0
    DECK = 1
    HAND = 2
    DESK = 3
    CEMETERY = 4  # This location may useless: cards in cemetery are only stored as card_id (?).

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

    # Does this card have a target?
    have_target = False

    def __init__(self, game, **kwargs):
        super().__init__(game)


class Minion(Card):
    """[NO_DESCRIPTION]

    The class of minion.
    """

    _data = {
        'taunt': False,
        'charge': False,
        'divine_shield': False,
        'stealth': False,
        'windfury': False,
        'poisonous': False,
        'lifesteal': False,
    }


class Spell(Card):
    pass


class Weapon(Card):
    pass


class HeroCard(Card):
    pass
