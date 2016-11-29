#! /usr/bin/python
# -*- encoding: utf-8 -*-

import unittest

from HearthStone.game_data import allCards

__author__ = 'fyabc'


class TestCardData(unittest.TestCase):
    def setUp(self):
        self.card0 = allCards[0]
        print(allCards)

    def test_card_attributes(self):
        self.assertEqual(self.card0.cost, 1)
        self.assertEqual(self.card0.attack, 2)
        self.assertEqual(self.card0.durability, 1)


def _test_card_data():
    import pprint
    pprint.pprint(allCards)

    card0 = allCards[0]
    print(card0.cost, card0.attack, card0.durability)


if __name__ == '__main__':
    prefix = '_test'
    for name in dir():
        if name.startswith(prefix):
            exec('{}()'.format(name))
