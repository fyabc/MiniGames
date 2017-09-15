#! /usr/bin/python
# -*- coding: utf-8 -*-

from .game_entity import GameEntity, SetDataMeta

__author__ = 'fyabc'


class Card(GameEntity, metaclass=SetDataMeta):
    """[NO_DESCRIPTION]

    The class of card.
    """

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

    def __init__(self, game, player_id):
        super().__init__(game)

        self.zone = 0
        self.player_id = player_id
        self.cost = self.data['CAH'][0]
        self.to_be_destroyed = False  # The destroy tag for instant kill enchantments.

    def __repr__(self):
        return super()._repr(id=self.data['id'], P=self.player_id)

    def check_target(self, target):
        """Check the validity of the target."""

        return True


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

    def __init__(self, game, player_id):
        super().__init__(game, player_id)

        self.attack = self.data['CAH'][1]
        self.health = self.data['CAH'][2]
        self.max_health = self.health
        self.to_be_destroyed = False  # The destroy tag for instant kill enchantments.


class Spell(Card):
    """[NO_DESCRIPTION]

    The class of spell.
    """

    _data = {
        'secret': False,
    }

    def run(self, target):
        """Run the spell.

        :param target:
        :return: list of events.
        """

        return []


class Weapon(Card):
    """[NO_DESCRIPTION]

    The class of weapon.
    """

    def __init__(self, game, player_id):
        super().__init__(game, player_id)

        self.attack = self.data['CAH'][1]
        self.health = self.data['CAH'][2]
        self.max_health = self.health


class HeroCard(Card):
    pass
