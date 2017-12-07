#! /usr/bin/python
# -*- coding: utf-8 -*-

from .game_entity import GameEntity, SetDataMeta
from ..utils.game import Zone

__author__ = 'fyabc'


class Card(GameEntity, metaclass=SetDataMeta):
    """The class of card."""

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

    have_target = False     # Does this card have a target?

    def __init__(self, game, player_id):
        super().__init__(game)

        self.zone = Zone.Invalid
        self.player_id = player_id
        self.cost = self.data['CAH'][0]
        self.orig_cost = self.data['CAH'][0]    # The original cost.
        self.to_be_destroyed = False  # The destroy tag for instant kill enchantments.

    def __repr__(self):
        return super()._repr(id=self.data['id'], P=self.player_id, oop=self.oop)

    def check_target(self, target):
        """Check the validity of the target."""

        return True

    @property
    def name(self):
        return self.data['name']

    @property
    def description(self):
        return self.data['description']

    @property
    def type(self):
        return self.data['type']

    @property
    def klass(self):
        return self.data['klass']

    @property
    def rarity(self):
        return self.data['rarity']


class Minion(Card):
    """The class of minion."""

    _data = {
        'taunt': False,
        'charge': False,
        'divine_shield': False,
        'stealth': False,
        'windfury': False,
        'poisonous': False,
        'lifesteal': False,
        'spell_power': 0,

        'battlecry': False,
        'deathrattle': False,
    }

    def __init__(self, game, player_id):
        super().__init__(game, player_id)

        self.attack = self.data['CAH'][1]
        self.health = self.data['CAH'][2]
        self.orig_health = self.data['CAH'][2]      # The original health.
        self.max_health = self.health
        self.to_be_destroyed = False  # The destroy tag for instant kill enchantments.

    def battlecry(self, target):
        """Run the battlecry. Implemented in subclasses.

        :param target: Target of the battlecry.
        :return: list of events.
        """

        return []


class Spell(Card):
    """The class of spell."""

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
    """The class of weapon."""

    def __init__(self, game, player_id):
        super().__init__(game, player_id)

        self.attack = self.data['CAH'][1]
        self.health = self.data['CAH'][2]
        self.orig_health = self.data['CAH'][2]  # The original health.
        self.max_health = self.health


class HeroCard(Card):
    """The class of hero card."""

    def __init__(self, game, player_id):
        super().__init__(game, player_id)

        self.armor = self.data['CAH'][1]
