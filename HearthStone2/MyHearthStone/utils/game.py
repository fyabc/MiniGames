#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'fyabc'


def order_of_play(objects):
    """Sort objects by the order of play.

    :param objects: Entities or events or triggers.
    :return: List of objects, sorted by order of play.
    """

    return sorted(objects, key=lambda o: o.oop)


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

    Str2Idx = {
        'Invalid': Invalid,
        'Deck': Deck,
        'Hand': Hand,
        'Play': Play,
        'Secret': Secret,
        'Graveyard': Graveyard,
        'SetAside': SetAside,
        'Weapon': Weapon,
    }

    Idx2Str = {v: k for k, v in Str2Idx.items()}


__all__ = [
    'order_of_play',
    'Zone',
]
