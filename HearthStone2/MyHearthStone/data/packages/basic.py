#! /usr/bin/python
# -*- coding: utf-8 -*-

"""Basic package, include basic cards and heroes."""

from MyHearthStone.ext import Spell, Hero

__author__ = 'fyabc'


class 幸运币(Spell):
    _data = {
        'id': 0,
    }
    pass


class Druid(Hero):
    _data = {
        'id': 0,
    }


class Hunter(Hero):
    _data = {
        'id': 1,
    }


class Mage(Hero):
    _data = {
        'id': 2,
    }


class Paladin(Hero):
    _data = {
        'id': 3,
    }


class Priest(Hero):
    _data = {
        'id': 4,
    }


class Rogue(Hero):
    _data = {
        'id': 5,
    }


class Shaman(Hero):
    _data = {
        'id': 6,
    }


class Warlock(Hero):
    _data = {
        'id': 7,
    }


class Warrior(Hero):
    _data = {
        'id': 8,
    }
