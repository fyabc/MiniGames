#! /usr/bin/python
# -*- coding: utf-8 -*-

import sys
from collections import ChainMap
from types import new_class

from .entity import GameEntity
from ..game_handlers.damage_handlers import SpellPowerHandler
from ..utils.basic_utils import find_index

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

    # Is this spell have target?
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

    def __init__(self, game, **kwargs):
        super(Minion, self).__init__(game, **kwargs)

        self.health = self.data['CAH'][2]           # Health

        self.remain_attack_number = 0               # Remain attack number in this turn
        self.divine_shield = False                  # Is this minion have divine shield?
        self.stealth = False
        self._frozen = 0                            # Is this minion frozen?
        self._silent = False                        # Is this minion silent?

        # Set spell power handlers.
        if self.data['spell_power'] > 0:
            self.handlers.add(SpellPowerHandler(self.game, self))

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
    def frozen(self):
        return self._frozen > 0

    @property
    def spell_power(self):
        if self._silent:
            result = 0
        else:
            result = self.data['spell_power']

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
    def run_battle_cry(self, player_id, index):
        """Override by subclasses.

        :param player_id: the player id.
        :param index: The location of the minion to be placed.
        """
        pass

    def run_death_rattle(self, player_id, index):
        """Override by subclasses.

        :param player_id: the player id.
        :param index: The original location of the dead minion.
        """
        pass

    def take_damage(self, source, value, event):
        if value <= 0:
            event.disable()
            return False
        if self.divine_shield:
            # [NOTE] When breaking the divine shield, it will not really cause damage, so disable it.
            self.divine_shield = False
            event.disable()
            return False
        else:
            self.health -= value
            return self.health <= 0

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
        """When a new turn start, refresh its attack number and frozen status.

        (Only when the minion is on the desk)
        """

        if self.location != self.DESK:
            return

        self._frozen_step()

        if self._frozen == 0:
            self.remain_attack_number = self.attack_number
        else:
            self.remain_attack_number = 0

    def turn_end(self):
        if self.location != self.DESK:
            return

        self.remain_attack_number = 0

    def freeze(self):
        # (2 = frozen next turn, 1 = frozen this turn, 0 = not frozen)
        self._frozen = 2
        self.remain_attack_number = 0

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

    def validate_target(self, player_id, location, index):
        """Test the legitimacy of the target.

        :param player_id:
        :param location:
        :param index:
        :return: True if the target is valid. String of message if invalid.
        """

        player = self.game.players[player_id]

        if player.remain_crystal >= self.cost:
            return True
        else:
            return 'I don\'t have enough mana crystals!'


class Weapon(Card):
    pass


__all__ = [
    'Card',
    'Minion',
    'Spell',
    'Weapon',
]
