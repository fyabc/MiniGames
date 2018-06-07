#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'fyabc'


OOP_LAST = (1 << 32) - 1


def order_of_play(objects, key=None, reverse=False):
    """Sort objects by the order of play.

    :param objects: Entities or events or triggers.
    :param key: User-defined key function.
    :param reverse: Sort in reversed order.
    :return: List of objects, sorted by order of play.
    """

    # If real oop is None, it means the entity is not played, so it have the lowest priority.
    def _default_key(o):
        return OOP_LAST if o.oop is None else o.oop

    if key is None:
        key = _default_key

    return sorted(objects, key=key, reverse=reverse)


class EnumMeta(type):
    @staticmethod
    def __new__(mcs, name, bases, ns):
        str2idx = {k: v for k, v in ns.items() if not k.startswith('_')}
        idx2str = {v: k for k, v in str2idx.items()}
        ns['Str2Idx'] = str2idx
        ns['Idx2Str'] = idx2str

        return super().__new__(mcs, name, bases, ns)


class Type(metaclass=EnumMeta):
    """An enumeration class, contains card types."""

    Invalid = -1
    Minion = 0
    Spell = 1
    Weapon = 2
    HeroCard = 3
    Permanent = 4   # Permanent card, such as the seed of 'Sherazin, Corpse Flower'.
    Game = 5
    Hero = 6
    Player = 7      # TODO: Differences between hero, player and weapon?
    Enchantment = 8
    Item = 9
    Token = 10
    HeroPower = 11


class Zone(metaclass=EnumMeta):
    """An enumeration class, contains zones of the card."""

    Invalid = 0
    Deck = 1
    Hand = 2
    Play = 3
    Secret = 4
    Graveyard = 5
    SetAside = 6
    Weapon = 7
    Hero = 8
    HeroPower = 9

    # Removed From Game Zone, holds enchantments that have expired, been detached or been silenced off.
    # TODO: Implement this zone.
    RFG = 10


class Rarity(metaclass=EnumMeta):
    """An enumeration class, contains rarities."""

    Derivative = -1
    Basic = 0
    Common = 1
    Rare = 2
    Epic = 3
    Legend = 4


class Race(metaclass=EnumMeta):
    """An enumeration class, contains races."""

    Beast = 0
    Murloc = 1
    Mech = 2
    Demon = 3
    Dragon = 4
    Totem = 5
    Elemental = 6


class Klass(metaclass=EnumMeta):
    """An enumeration class, contains classes."""

    Neutral = 0
    Druid = 1
    Hunter = 2
    Mage = 3
    Paladin = 4
    Priest = 5
    Rogue = 6
    Shaman = 7
    Warlock = 8
    Warrior = 9
    Monk = 10
    DeathKnight = 11


# Map classes to heroes (which hero to use for each class).
# TODO: Remove hard code here
DefaultClassHeroMap = {
    1: 0,
    2: 1,
    3: 2,
    4: 3,
    5: 4,
    6: 5,
    7: 6,
    8: 7,
    9: 8,
    10: 9,
    11: 10,
}


class AuraType(metaclass=EnumMeta):
    """An enumeration class, contains aura types."""
    AttackHealth = 0
    Other = 1


class Condition:
    """The class of conditions to get random cards or select cards."""

    pass


__all__ = [
    'order_of_play',

    'EnumMeta',
    'Type', 'Zone', 'Rarity', 'Race', 'Klass',
    'AuraType',
    'Condition',

    'DefaultClassHeroMap',
]
