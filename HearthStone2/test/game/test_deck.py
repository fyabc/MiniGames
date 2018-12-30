#! /usr/bin/python
# -*- coding: utf-8 -*-

import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))

from MyHearthStone.game.deck import Deck
from MyHearthStone.utils.game import Klass

from . import utils

__author__ = 'fyabc'


class TestDeck(unittest.TestCase):
    test_deck = None

    @classmethod
    def setUpClass(cls):
        cls.test_deck = utils.ExampleDecks[0]

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def _assertDeckSame(self, deck):
        self.assertEqual(self.test_deck.mode, deck.mode)
        self.assertEqual(self.test_deck.klass, deck.klass)
        self.assertListEqual(self.test_deck.card_id_list, deck.card_id_list)
        self.assertEqual(self.test_deck.name, deck.name)

    def testBasic(self):
        self.assertEqual(str(self.test_deck), "Deck(class=Mage, name='Test Mage', mode=standard)")

    def testCopy(self):
        self._assertDeckSame(self.test_deck.copy())

    def testCodeIO(self):
        new_deck = Deck.from_code(self.test_deck.to_code())
        self._assertDeckSame(new_deck)
