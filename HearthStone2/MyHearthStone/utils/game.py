#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'fyabc'


def order_of_play(objects):
    """Sort objects by the order of play.

    :param objects: Entities or events or triggers.
    :return: List of objects, sorted by order of play.
    """

    return sorted(objects, key=lambda o: o.oop)


def error_and_stop(game, event, msg):
    """Show an error message and stop the event.

    :param game:
    :param event:
    :param msg:
    :return:
    """

    game.error_stub(msg)
    event.disable()
    game.stop_subsequent_phases()


# TODO: change these classes into ``enum.IntEnum``?


class Type:
    """An enumeration class, contains card types."""

    Minion = 0
    Spell = 1
    Weapon = 2
    HeroCard = 3
    Permanent = 4   # Permanent card, such as the seed of 'Sherazin, Corpse Flower'.

    # todo


class Zone:
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

    Str2Idx = {
        'Invalid': Invalid,
        'Deck': Deck,
        'Hand': Hand,
        'Play': Play,
        'Secret': Secret,
        'Graveyard': Graveyard,
        'SetAside': SetAside,
        'Weapon': Weapon,
        'Hero': Hero,
    }

    Idx2Str = {v: k for k, v in Str2Idx.items()}


class Rarity:
    """An enumeration class, contains rarities."""

    Derivative = -1
    Basic = 0
    Common = 1
    Rare = 2
    Epic = 3
    Legend = 4

    Str2Idx = {
        'Derivative': Derivative,
        'Basic': Basic,
        'Common': Common,
        'Rare': Rare,
        'Epic': Epic,
        'Legend': Legend,
    }

    Idx2Str = {v: k for k, v in Str2Idx.items()}


class Race:
    """An enumeration class, contains races."""

    Beast = 0
    Murloc = 1
    Mech = 2
    Demon = 3
    Dragon = 4
    Totem = 5
    Elemental = 6

    Str2Idx = {
        'Beast': Beast,
        'Murloc': Murloc,
        'Mech': Mech,
        'Demon': Demon,
        'Dragon': Dragon,
        'Totem': Totem,
        'Elemental': Elemental,
    }

    Idx2Str = {v: k for k, v in Str2Idx.items()}


class Klass:
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

    Str2Idx = {
        'Neutral': Neutral,
        'Druid': Druid,
        'Hunter': Hunter,
        'Mage': Mage,
        'Paladin': Paladin,
        'Priest': Priest,
        'Rogue': Rogue,
        'Shaman': Shaman,
        'Warlock': Warlock,
        'Warrior': Warrior,
        'Monk': Monk,
        'DeathKnight': DeathKnight,
    }

    Idx2Str = {v: k for k, v in Str2Idx.items()}


class Condition:
    """The class of conditions to get random cards or select cards."""

    pass


__all__ = [
    'order_of_play',
    'error_and_stop',
    'Type',
    'Zone',
    'Rarity',
    'Race',
    'Klass',
    'Condition',
]
