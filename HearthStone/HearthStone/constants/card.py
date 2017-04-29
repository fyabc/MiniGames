#! /usr/bin/python
# -*- encoding: utf-8 -*-

"""Constants of the card."""

__author__ = 'fyabc'


# Type: 0 = minion, 1 = spell, 2 = weapon
Type_minion = 0
Type_spell = 1
Type_weapon = 2
Type_player = 3

# Rarity: 0 = basic, 1 = common, 2 = rare, 3 = epic, 4 = legend, -1 = derivative
Rarity_basic = 0
Rarity_common = 1
Rarity_rare = 2
Rarity_epic = 3
Rarity_legendary = 4
Rarity_derivative = -1

# Klass: 0 = neutral, others are class id.
Klass_neutral = 0
Klass_mage = 1
Klass_rogue = 2
Klass_priest = 3
Klass_warlock = 4
Klass_warrior = 5
Klass_hunter = 6
Klass_shaman = 7
Klass_paladin = 8
Klass_druid = 9

# Race: to be stored into database, it can be mapped to single char.
Races = {
    'Beast': '0',
    'Murloc': '1',
    'Pirate': '2',
    'Mech': '3',
    'Dragon': '4',
    'Devil': '5',
    'Totem': '6',
    'Elemental': '7',
}

ReversedRaces = {v: k for k, v in Races.items()}


def race2str(races):
    return ''.join(Races[race] for race in races)


def str2race(races_str):
    return [ReversedRaces[race_str] for race_str in races_str]


# Locations of the card.
Location_NULL = 0
Location_DECK = 1
Location_HAND = 2
Location_DESK = 3
Location_CEMETERY = 4
