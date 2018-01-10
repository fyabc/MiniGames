#! /usr/bin/python
# -*- coding: utf-8 -*-

import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from MyHearthStone.utils import package_io as pio
from MyHearthStone.game.card import Spell

__author__ = 'fyabc'


class TestPackageIO(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testAllCards(self):
        all_cards = pio.all_cards()

        self.assertIn(0, all_cards)         # 幸运币
        self.assertIn(7, all_cards)         # 工程师学徒
        self.assertIn(30008, all_cards)     # 火球术
        self.assertIn(90001, all_cards)     # 炽炎战斧

    def testOneCard(self):
        Fireball = pio.all_cards()[30008]

        self.assertTrue(issubclass(Fireball, Spell))
        self.assertListEqual(Fireball.data['CAH'], [4])
