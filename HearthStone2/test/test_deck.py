#! /usr/bin/python
# -*- coding: utf-8 -*-

import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from MyHearthStone.game.deck import Deck
from MyHearthStone.utils.game import Klass

__author__ = 'fyabc'


class TestDeck(unittest.TestCase):
    test_deck = None

    @classmethod
    def setUpClass(cls):
        cls.test_deck = Deck(klass=Klass.Str2Idx['Druid'], card_id_list=[
            6, 6, 6, 6,
            11, 11, 11, 11,
            10000, 10000, 10000, 10000,
            30007, 30007, 30007, 30007,
        ], name='Test Druid')

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testBasic(self):
        self.assertEqual(str(self.test_deck), "Deck(class=Druid, name='Test Druid', mode=standard)")
