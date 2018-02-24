#! /usr/bin/python
# -*- coding: utf-8 -*-

"""The base class of game entities."""

from collections import ChainMap

from ..utils.message import entity_message

__author__ = 'fyabc'


class SetDataMeta(type):
    """This metaclass is used for setting `data` attribute of cards automatically.

    This metaclass will set the `data` attribute with a new `ChainMap` instance
    (if its last base class does not have `data` attribute) or the `data` attribute
    of its last base class if it has `data` attribute.
    The value of new child of `data` is stored in `data` attribute of the class.
    """

    @staticmethod
    def __new__(mcs, name, bases, ns):
        # This called before the class created.
        # print('New:', mcs, name, bases, ns)

        base_data = getattr(bases[-1], 'data', None) if bases else None
        this_data = ns.get('data', {})
        ns['data'] = base_data.new_child(this_data) if base_data is not None else ChainMap(this_data)

        return super().__new__(mcs, name, bases, ns)

    def __init__(cls, name, bases, ns):
        # This called after the class created.
        # print('Init:', cls, name, bases, ns)

        super().__init__(name, bases, ns)


class GameEntity(metaclass=SetDataMeta):
    """The base class of all game entities.

    [NOTE]:
        Use `CardClass.data['cost']` to access class-level data (original card data, will not be changed).
        Use `card_object.cost` to access object-level data (card-specific data, may be changed in the game).
    """

    data = {
        'version': None,
        'id': None,
        'name': '',
        'package': 0,
        'description': '',
    }

    def __init__(self, game):
        self.game = game

        # oop(Order Of Play).
        # All game entities have this attribute, and share the same oop list.
        self.oop = None

        # Enchantment list of this entity.
        self.enchantments = []

    def _repr(self, **kwargs):
        __show_cls = kwargs.pop('__show_cls', True)
        return entity_message(self, kwargs, prefix='#', __show_cls=__show_cls)

    def __repr__(self):
        return self._repr()

    @property
    def id(self):
        return self.data['id']

    @property
    def name(self):
        return self.data['name']

    @property
    def description(self):
        # todo: Apply enchantments that affect description (e.g. spell power) on it.
        return self.data['description']

    @classmethod
    def get_cahr(cls):
        """Get cost / attack / health / armor (basic attributes)."""
        result = []
        if 'cost' in cls.data:
            result.append(cls.data['cost'])
        if 'attack' in cls.data:
            result.append(cls.data['attack'])
        if 'health' in cls.data:
            result.append(cls.data['health'])
        if 'armor' in cls.data:
            result.append(cls.data['armor'])
        return result

    def add_enchantment(self, enchantment):
        # todo: insert it in order of play.
        self.enchantments.append(enchantment)

    def aura_update_attack_health(self):
        """Aura update (attack / health), called by the same method of class `Game`."""
        # todo: Move auras to the end, and more.
        # See <https://hearthstone.gamepedia.com/Advanced_rulebook#Auras> for details.
        for enchantment in self.enchantments:
            enchantment.apply()
