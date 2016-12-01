#! /usr/bin/python
# -*- encoding: utf-8 -*-

"""File of data of this game.
It contains card data, etc.
"""

import os
import json

from .utils import CardDataPath, HeroDataPath

__author__ = 'fyabc'


class DataClass:
    attributes = {}

    def __init__(self):
        self.__dict__.update(self.attributes)

    def __str__(self):
        return '{}({})'.format(
            self.__class__.__name__,
            ','.join('{}={}'.format(k, v) for k, v in self.__dict__.items()))

    def __repr__(self):
        return self.__str__()

    @classmethod
    def from_dict(cls, data):
        result = cls.__new__(cls)
        result.__dict__.update(cls.attributes)
        result.__dict__.update(data)
        return result

    @classmethod
    def load_all(cls, dir_name, dict_entry):
        result = {}

        for package_filename in os.listdir(dir_name):
            if not package_filename.endswith('.json'):
                continue
            with open(os.path.join(dir_name, package_filename), 'r', encoding='utf-8') as package_file:
                package_dict = json.load(package_file)

                for card_dict in package_dict[dict_entry]:
                    card_data = cls.from_dict(card_dict)
                    result[card_data.id] = card_data

        return result


class CardData(DataClass):
    attributes = {
        'id': 0,
        'name': "",
        'CAH': None,
        'skills': [],
        'taunt': False,
        'charge': False,
        'divine_shield': False,
        'attack_number': 1,
    }

    @property
    def cost(self):
        return self.CAH[0]

    @property
    def attack(self):
        if len(self.CAH) >= 2:
            return self.CAH[1]
        return None

    @property
    def health(self):
        if len(self.CAH) >= 3:
            return self.CAH[2]
        return None

    durability = health

    @classmethod
    def from_dict(cls, data):
        result = super().from_dict(data)

        # todo: parse skills

        return result


class HeroData(DataClass):
    attributes = {
        "id": 0,
        "klass": "",
        "health": 30,
        "skill": None,
    }

    @classmethod
    def from_dict(cls, data):
        result = super().from_dict(data)

        # todo: parse skills

        return result


# Automatically load some data at begin of the game.
allCards = CardData.load_all(CardDataPath, 'cards')
allHeroes = HeroData.load_all(HeroDataPath, 'heroes')
