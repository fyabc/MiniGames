#! /usr/bin/python
# -*- encoding: utf-8 -*-

import unittest

from HearthStone.game_data import allCards

__author__ = 'fyabc'


class TestCardData(unittest.TestCase):
    pass


def _test_card_data():
    print(allCards)

    card0 = allCards[0]
    print(card0.cost, card0.attack, card0.durability)


def run_all_tests(prefix='_test'):
    for name in dir():
        if name.startswith(prefix):
            exec('{}()'.format(name))


if __name__ == '__main__':
    run_all_tests()
