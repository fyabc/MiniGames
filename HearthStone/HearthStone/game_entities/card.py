#! /usr/bin/python
# -*- coding: utf-8 -*-

import sys
from collections import ChainMap
from types import new_class

from .entity import GameEntity
from .minion_like import IMinion
from ..game_handlers.damage import SpellPowerHandler
from ..utils.basic import find_index

__author__ = 'fyabc'


class SetDataMeta(type):
    @staticmethod
    def __new__(mcs, name, bases, ns):
        # This called before the class created.
        # print('New:', mcs, name, bases, ns)

        # assert len(bases) == 1, 'This metaclass requires the class have exactly 1 superclass.'

        base_data = getattr(bases[0], 'data', ChainMap())
        ns['data'] = base_data.new_child(ns.get('_data', {}))

        doc = ns.get('__doc__', None)
        if doc is not None and not doc.startswith('[NO_DESCRIPTION]'):
            ns['data']['description'] = doc

        return type.__new__(mcs, name, bases, ns)

    def __init__(cls, name, bases, ns):
        # This called after the class created.
        # print('Init:', cls, name, bases, ns)

        super().__init__(name, bases, ns)


class Card(GameEntity, metaclass=SetDataMeta):
    """[NO_DESCRIPTION]

    The class of card.

    [NOTE] We do not copy the value of cost from CardData into card.
        Reason: see docstring of `Minion`.
    """

    CreatedCardNumber = 0

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

    # Is this card have target?
    have_target = False

    def __init__(self, game, **kwargs):
        super(Card, self).__init__(game)

        self.id = Card.CreatedCardNumber
        Card.CreatedCardNumber += 1

        # Card data.
        self.location = self.NULL

        # Auras on this card.
        # These auras will affect cost, attack and other attributes of card.
        self.auras = []

        # Handlers of this card.
        # [NOTE] Thinking: How to apply these handlers?
        #   For a handler `h` which should run on desk:
        #       1. enable it when the card is put onto the desk.
        #       2. disable it (and reset it?) when the card it remove from the desk.
        self.handlers = set()

        # todo: add card creator.
        self.creator = None

        player_id = kwargs.pop('player_id', None)
        if player_id is not None:
            self._player_id = player_id

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
    def overload(self):
        result = self.data['overload']

        # todo: add auras

        return result

    @property
    def type(self):
        return self.data['type']

    @property
    def race(self):
        return self.data['race']

    @property
    def player_id(self):
        if hasattr(self, '_player_id'):
            return self._player_id

        if self.location == self.NULL:
            return None
        else:
            p0, p1 = self.game.players

            if self.location == self.DECK:
                return 0 if self in p0.deck else 1
            elif self.location == self.HAND:
                return 0 if self in p0.hand else 1
            elif self.location == self.DESK:
                return 0 if self in p0.desk else 1
            else:
                return None

    # Hook methods on location change. To be implemented in subclasses.
    def change_location(self, location, *args, **kwargs):
        """Change the location of the card, and call some hook methods.

        :param location: the new location to be changed to.
        :param args: some arguments to be passed, (e.g. index and player_id in changing to desk)
        :param kwargs: such as args.
        :return:
        """

        raise NotImplementedError()

    # Some utilities.
    def get_selection(self):
        for player_id in (0, 1):
            player = self.game.players[player_id]

            index = find_index(player.deck, self)
            if index is not None:
                return player_id, 'deck', index

            index = find_index(player.hand, self)
            if index is not None:
                return player_id, 'hand', index

            index = find_index(player.desk, self)
            if index is not None:
                return player_id, 'desk', index
        return None

    @classmethod
    def create_blank(cls, name, data):
        cls_dict = {'_data': data}
        result = new_class(name, (cls,), {}, lambda ns: ns.update(cls_dict))

        # Get the module name of caller.
        result.__module__ = sys._getframe(1).f_globals['__name__']
        return result

    def validate_target(self, target):
        """Test the legitimacy of the target.

        :param target: The target of the spell. None if there is not any target.
        :return: True if the target is valid. String of message if invalid.
        """

        player = self.game.players[self.player_id]

        if player.remain_crystal >= self.cost:
            return True
        else:
            return 'I don\'t have enough mana crystals!'


class Minion(Card, IMinion):
    """[NO_DESCRIPTION]

    The class of minion.

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

    def __init__(self, game, **kwargs):
        super(Minion, self).__init__(game, **kwargs)

        self.health = self.data['CAH'][2]           # Health

        self.remain_attack_number = 0               # Remain attack number in this turn
        self.divine_shield = False                  # Is this minion have divine shield?
        self.stealth = False
        self._frozen = 0                            # Is this minion frozen?
        self._silent = False                        # Is this minion silent?

        self.timestamp = None                       # The timestamp of the minion to summon to the desk.

        # Set spell power handlers.
        if self.data['spell_power'] > 0:
            self.handlers.add(SpellPowerHandler(self.game, self))

    def __str__(self):
        return '{}({},{},{})'.format(self.data['name'], self.cost, self.attack, self.health)

    # Properties.

    @property
    def alive(self):
        return self.health > 0

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
    def spell_power(self):
        if self._silent:
            result = 0
        else:
            result = self.data['spell_power']

        # todo: add auras

        return result

    # Some internal methods.
    def change_location(self, location, *args, **kwargs):
        if self.location == self.NULL:
            pass
        elif self.location == self.DECK:
            pass
        elif self.location == self.HAND:
            pass
        elif self.location == self.DESK:
            pass
        elif self.location == self.CEMETERY:
            pass

        # Trigger all handlers of this card.
        for handler in self.handlers:
            handler.trigger(self.location, location)

        self.location = location

        if location == self.NULL:
            pass
        elif location == self.DECK:
            pass
        elif location == self.HAND:
            pass
        elif location == self.DESK:
            # Initializations of the minion before put onto desk. (Both summon and put directly)
            if self.charge:
                self.remain_attack_number = self.attack_number
            else:
                self.remain_attack_number = 0
            self.divine_shield = self.data['divine_shield']
        elif location == self.CEMETERY:
            pass

    # Operations.
    def run_battle_cry(self, player_id, index, target=None):
        """Override by subclasses. Default is do nothing.

        :param player_id: the player id.
        :param index: The location of the minion to be placed.
        :param target: Optional, the target of battle cry.
            Example: If the battle cry is deal 1 damage to the target, this parameter is needed.
        """
        pass

    def run_death_rattle(self, player_id, index):
        """Override by subclasses.

        :param player_id: the player id.
        :param index: The original location of the dead minion.
        """
        pass

    def silence(self):
        """Silence the minion."""

        self._silent = True
        self.auras.clear()

        # Reset health.
        self._fit_health()

        self._frozen = 0
        self.divine_shield = False
        self.stealth = False

    def turn_begin(self):
        if self.location != self.DESK:
            return

        self._minion_turn_begin()

    def turn_end(self):
        if self.location != self.DESK:
            return

        self._minion_turn_end()

    # Some other methods.
    def add_aura(self, aura):
        self.auras.append(aura)

    def remove_dead_auras(self):
        pass


class Spell(Card):
    def __init__(self, game, **kwargs):
        super().__init__(game, **kwargs)

    def __str__(self):
        return '{}({})'.format(self.data['name'], self.cost)

    def change_location(self, location, *args, **kwargs):
        if self.location == self.NULL:
            pass
        elif self.location == self.DECK:
            pass
        elif self.location == self.HAND:
            pass
        elif self.location == self.CEMETERY:
            pass

        # Trigger all handlers of this card.
        for handler in self.handlers:
            handler.trigger(self.location, location)

        self.location = location

        if location == self.NULL:
            pass
        elif location == self.DECK:
            pass
        elif location == self.HAND:
            pass
        elif location == self.CEMETERY:
            pass

    def play(self, player_id, target):
        """Override by subclasses.

        :param player_id: The id of the spell player.
        :param target: The target of this spell. None if the spell doesn't have any target.
        """

        pass


class Weapon(Card):
    pass


__all__ = [
    'Card',
    'Minion',
    'Spell',
    'Weapon',
]
