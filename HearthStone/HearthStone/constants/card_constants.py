#! /usr/bin/python
# -*- encoding: utf-8 -*-

"""Constants of the card."""

__author__ = 'fyabc'


# Type: 0 = minion, 1 = spell, 2 = weapon
Type_minion = 0
Type_spell = 1
Type_weapon = 2

# Rarity: 0 = basic, 1 = common, 2 = rare, 3 = epic, 4 = legend, -1 = derivative
Rarity_basic = 0
Rarity_common = 1
Rarity_rare = 2
Rarity_epic = 3
Rarity_legendary = 4
Rarity_derivative = -1

# Klass: 0 = neutral, others are class id.
Klass_neutral = 0

# Race: to be stored into database, it can be mapped to single char.
Races = {
    'Beast': '0',
    'Murloc': '1',
    'Pirate': '2',
    'Mech': '3',
    'Dragon': '4',
}

ReversedRaces = {v: k for k, v in Races.items()}


def race2str(races):
    return ''.join(Races[race] for race in races)


def str2race(races_str):
    return [ReversedRaces[race_str] for race_str in races_str]
