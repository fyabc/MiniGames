#! /usr/bin/python
# -*- coding: utf-8 -*-

from collections import ChainMap
from types import new_class

from .entity import GameEntity

__author__ = 'fyabc'


class SetDataMeta(type):
    @staticmethod
    def __new__(mcs, name, bases, ns):
        # This called before the class created.
        # print('New:', mcs, name, bases, ns)

        assert len(bases) == 1, 'This metaclass requires the class have exactly 1 superclass.'

        base_data = getattr(bases[0], 'data', ChainMap())
        ns['data'] = base_data.new_child(ns.get('_data', {}))

        return type.__new__(mcs, name, bases, ns)

    def __init__(cls, name, bases, ns):
        # This called after the class created.
        # print('Init:', cls, name, bases, ns)

        super().__init__(name, bases, ns)


class Card(GameEntity, metaclass=SetDataMeta):
    """The class of card.

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

    2. Create a file
        Create a Python file into the user card data path.

        It is recommended that the file name is same as the package name, so you should create a file `package001.py`.

        Your extension directory is like this:
        my_HS_extension/
            HearthStoneCard/
                package001.py
            HearthStoneHeroes/      (This directory can be omitted now)



    Docstring for the HearthStone system
    ====================================

    [NOTE] We do not copy the value of cost from CardData into card.
        Reason: see docstring of `Minion`.
    """

    CreatedCardNumber = 0

    # Types of the card.
    Type_Minion = 0
    Type_Spell = 1
    Type_Weapon = 2

    # Locations of the card.
    Null = 0
    Deck = 1
    Hand = 2
    Desk = 3
    Cemetery = 4  # This location may useless: cards in cemetery are only stored as card_id (?).

    _data = {
        'id': None,
        'type': 0,
        'name': '',
        'package': 0,
        'rarity': 0,
        'klass': 0,             # The class of the card: 0 is neutral, others are class id.
        'race': [],
        'CAH': [0, 1, 1],
        'overload': 0,
    }

    data = {}

    def __init__(self, game):
        super(Card, self).__init__(game)

        self.id = Card.CreatedCardNumber
        Card.CreatedCardNumber += 1

        # Card data.
        self.location = self.Null

        # Auras on this card.
        # These auras will affect cost, attack and other attributes of card.
        self.auras = []

    def __str__(self):
        return '{}(id={},card_id={},name={})'.format(type(self).__name__, self.id, self.data['id'], self.data['name'])

    def __repr__(self):
        return self.__str__()

    # Properties.
    # [NOTE] In current, this property just return the cost itself.
    # But in future, there may be some auras on the card, so use property.
    # Such as other attributes.
    @property
    def cost(self):
        result = self.data['CAH'][0]

        # todo: add auras

        return result

    @property
    def player_id(self):
        # todo: check and return the player id of this card.
        # [NOTE] The card may be controlled by different players, so this property may change.
        return None

    # Some utilities.
    @classmethod
    def create_blank(cls, name, data):
        cls_dict = {'_data': data}
        result = new_class(name, (cls,), {}, lambda ns: ns.update(cls_dict))
        result.__module__ = __name__
        return result


class Minion(Card):
    """The class of minion.

    [NOTE] Attributes of the minion are affected by its auras (EXCEPT health)
        So we only need to save the health value,
        other attributes should be calculated by its basic value and auras.
    """

    _data = {
        'attack_number': 1,
        'taunt': False,
        'charge': False,
        'divine_shield': False,
        'stealth': False,
    }

    def __init__(self, game):
        super(Minion, self).__init__(game)

        self.health = self.data['CAH'][2]           # Health

        self.remain_attack_number = 0               # Remain attack number in this turn
        self._divine_shield = False                 # Is this minion have divine shield?
        self._frozen = 0                            # Is this minion frozen?
        self._silent = False                        # Is this minion silent?

    def __str__(self):
        return '{}({},{},{})'.format(self.data['name'], self.cost, self.attack, self.health)

    # Properties.
    @property
    def attack(self):
        result = self.data['CAH'][1]

        # todo: add auras

        return result

    @property
    def max_health(self):
        result = self.data['CAH'][2]

        # todo: add auras

        return result

    @property
    def attack_number(self):
        if self._silent:
            result = 1
        else:
            result = self.data['attack_number']

        # todo: add auras

        return result

    @property
    def divine_shield(self):
        if self._silent:
            result = False
        else:
            result = self.data['divine_shield']

        # todo: add auras

        return result

    @property
    def taunt(self):
        if self._silent:
            result = False
        else:
            result = self.data['taunt']

        # todo: add auras

        return result

    @property
    def charge(self):
        if self._silent:
            result = False
        else:
            result = self.data['charge']

        # todo: add auras

        return result

    @property
    def stealth(self):
        if self._silent:
            result = False
        else:
            result = self.data['stealth']

        # todo: add auras

        return result

    # Some internal methods.
    def _frozen_step(self):
        if self._frozen > 0:
            self._frozen -= 1

    def _fit_health(self):
        max_health = self.max_health
        if self.health > max_health:
            self.health = max_health

    # Operations.
    def init_before_hand(self):
        self.location = self.Hand

    def init_before_desk(self):
        """Initializations of the minion before put onto desk. (Both summon and put directly)"""
        self.remain_attack_number = self.attack_number
        self._divine_shield = self.divine_shield
        self.location = self.Desk

    def run_battle_cry(self):
        """Overrided by subclasses."""
        pass

    def death(self):
        pass

    def run_death_rattle(self):
        """Overrided by subclasses."""
        pass

    def take_damage(self, source, value):
        self.health -= value
        return self.health <= 0

    def silence(self):
        """Silence the minion."""

        self._silent = True
        self.auras.clear()

        # Reset health.
        self._fit_health()

        self._frozen = 0

    def turn_begin(self):
        """When a new turn start, refresh its attack number and frozen status."""

        self.remain_attack_number = self.attack_number
        self._frozen_step()

    def froze(self):
        # (2 = frozen next turn, 1 = frozen this turn, 0 = not frozen)
        self._frozen = 2

    # Some other methods.
    def add_aura(self, aura):
        self.auras.append(aura)

    def remove_dead_auras(self):
        pass


class Spell(Card):
    pass


class Weapon(Card):
    pass


__all__ = [
    'Card',
    'Minion',
    'Spell',
    'Weapon',
]
