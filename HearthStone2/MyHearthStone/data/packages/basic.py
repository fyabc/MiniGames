#! /usr/bin/python
# -*- coding: utf-8 -*-

"""Basic package, include basic cards and heroes."""

from MyHearthStone.ext import Spell, Hero
from MyHearthStone.ext import message as msg

__author__ = 'fyabc'


class 幸运币(Spell):
    _data = {
        'id': 0,
        'name': '幸运币',
        'rarity': -1,
        'CAH': [0],
    }

    def run(self, target):
        self.game.add_mana(1, '1', self.player_id)
        msg.verbose('Add 1 mana to player {} in this turn!'.format(self.player_id))

        return []


class Druid(Hero):
    _data = {
        'id': 0,
        'CAH': [None, None, 30],
    }


class Hunter(Hero):
    _data = {
        'id': 1,
        'CAH': [None, None, 30],
    }


class Mage(Hero):
    _data = {
        'id': 2,
        'CAH': [None, None, 30],
    }


class Paladin(Hero):
    _data = {
        'id': 3,
        'CAH': [None, None, 30],
    }


class Priest(Hero):
    _data = {
        'id': 4,
        'CAH': [None, None, 30],
    }


class Rogue(Hero):
    _data = {
        'id': 5,
        'CAH': [None, None, 30],
    }


class Shaman(Hero):
    _data = {
        'id': 6,
        'CAH': [None, None, 30],
    }


class Warlock(Hero):
    _data = {
        'id': 7,
        'CAH': [None, None, 30],
    }


class Warrior(Hero):
    _data = {
        'id': 8,
        'CAH': [None, None, 30],
    }
