#! /usr/bin/python
# -*- coding: utf-8 -*-

import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))

from MyHearthStone.game.core import Game
from MyHearthStone.game.player import Player
from MyHearthStone.game.deck import Deck
from MyHearthStone.utils.game import Klass

__author__ = 'fyabc'


class TestCore(unittest.TestCase):
    test_decks = [None, None]

    @classmethod
    def setUpClass(cls):
        cls.test_decks = [
            Deck(klass=Klass.Str2Idx['Druid'], card_id_list=[
                6, 6, 6, 6,
                11, 11, 11, 11,
                10000, 10000, 10000, 10000,
                30007, 30007, 30007, 30007,
            ], name='Test Druid'),
            Deck(klass=Klass.Str2Idx['Hunter'], card_id_list=[
                6, 6, 6, 6,
                11, 11, 11, 11,
                10000, 10000, 10000, 10000,
                30007, 30007, 30007, 30007,
            ], name='Test Hunter'),
        ]

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.game = Game()
        start_game_iter = self.game.start_game(self.test_decks, mode='standard')
        try:
            next(start_game_iter)
            start_game_iter.send([[], []])
        except StopIteration:
            pass

        self.p0, self.p1 = self.game.players[self.game.current_player], self.game.players[1 - self.game.current_player]

    def tearDown(self):
        self.game.end_game()

    # Game basic tests.

    def testBasic(self):
        self.assertIsInstance(self.p0, Player, 'Offensive player is not successfully created')
        self.assertIsInstance(self.p1, Player, 'Defensive player is not successfully created')

    def testZones(self):
        self.assertEqual(len(self.p0.hand), Player.StartCardOffensive + 1)
        self.assertEqual(len(self.p1.hand), Player.StartCardDefensive + 1)

    # Player action tests.

    def testTurnEnd(self):
        pass

    def testConcede(self):
        pass
