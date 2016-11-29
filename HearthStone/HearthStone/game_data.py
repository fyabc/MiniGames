#! /usr/bin/python
# -*- encoding: utf-8 -*-

"""File of data of this game.
It contains card data, etc.
"""

import os
import json

from HearthStone.utils import CardDataPath

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

    @staticmethod
    def load_all_cards(dir_name=CardDataPath):
        result = {}

        for package_filename in os.listdir(dir_name):
            if not package_filename.endswith('.json'):
                continue
            with open(os.path.join(dir_name, package_filename), 'r', encoding='utf-8') as package_file:
                package_dict = json.load(package_file)

                for card_dict in package_dict['cards']:
                    card_data = CardData.from_dict(card_dict)
                    result[card_data.id] = card_data

        return result

    @classmethod
    def get_default(cls, *attributes):
        return [cls.attributes[attribute] for attribute in attributes]


# Automatically load some data at begin of the game.
allCards = CardData.load_all_cards()
