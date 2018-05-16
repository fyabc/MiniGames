#! /usr/bin/python
# -*- coding: utf-8 -*-

import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))

from MyHearthStone.game.core import Game
from MyHearthStone.game.player import Player
from MyHearthStone.game.deck import Deck
from MyHearthStone.game import player_action as pa
from MyHearthStone.game.events import standard as std_e
from MyHearthStone.utils.game import Klass

__author__ = 'fyabc'


class TestCore(unittest.TestCase):
    test_decks = [None, None]

    game_start_events = [std_e.BeginOfGame, std_e.BeginOfTurn, std_e.DrawCard]

    @classmethod
    def setUpClass(cls):
        cls.test_decks = [
            Deck(klass=Klass.Str2Idx['Druid'], card_id_list=[
                "6", "6", "6", "6",
                "11", "11", "11", "11",
                "10000", "10000", "10000", "10000",
                "30007", "30007", "30007", "30007",
            ], name='Test Druid'),
            Deck(klass=Klass.Str2Idx['Hunter'], card_id_list=[
                "6", "6", "6", "6",
                "11", "11", "11", "11",
                "10000", "10000", "10000", "10000",
                "30007", "30007", "30007", "30007",
            ], name='Test Hunter'),
        ]

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.game = Game()
        self.game.start_game(self.test_decks, mode='standard')
        self.game.run_player_action(pa.ReplaceStartCard(self.game, 0, []))
        self.game.run_player_action(pa.ReplaceStartCard(self.game, 1, []))

        self.p0, self.p1 = self.game.players[self.game.current_player], self.game.players[1 - self.game.current_player]

    def _assertEventType(self, event_types):
        self.assertListEqual(event_types, [type(e) for e in self.game.event_history])

    def tearDown(self):
        self.game.end_game()

    # Game basic tests.

    def testBasic(self):
        self.assertEqual(self.game.state, self.game.GameState.Main, 'Game is not in main state')
        self.assertIsInstance(self.p0, Player, 'Offensive player is not successfully created')
        self.assertIsInstance(self.p1, Player, 'Defensive player is not successfully created')

    def testZones(self):
        self.assertEqual(len(self.p0.hand), Player.StartCardOffensive + 1)
        self.assertEqual(len(self.p1.hand), Player.StartCardDefensive + 1)

    def testGameStartEvents(self):
        self._assertEventType(self.game_start_events)

    # Player action tests.

    def testTurnEnd(self):
        player_before = self.game.current_player
        self.game.run_player_action(pa.TurnEnd(self.game))
        self.assertNotEqual(player_before, self.game.current_player)

        self._assertEventType(self.game_start_events + [std_e.EndOfTurn, std_e.BeginOfTurn, std_e.DrawCard])

    def testConcede(self):
        current_player = self.game.current_player
        self.game.run_player_action(pa.Concede(self.game))

        self._assertEventType(self.game_start_events + [std_e.HeroDeath])
        self.assertEqual(self.game.event_history[-1].owner.player_id, current_player)
