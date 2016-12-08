#! /usr/bin/python
# -*- encoding: utf-8 -*-

"""File of data of this game.
It contains card data, etc.
"""

from .data_class import DataClass
from ..utils import CardDataPath

__author__ = 'fyabc'


class CardData(DataClass):
    attributes = {
        'id': None,
        'name': "",
        "type": 0,
        'CAH': None,
        'skills': [],
        'taunt': False,
        'charge': False,
        'divine_shield': False,
        'stealth': False,
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


# Automatically load some data at begin of the game.
allCards = CardData.load_all(CardDataPath, 'cards')

__all__ = [
    'CardData',
    'allCards',
]
