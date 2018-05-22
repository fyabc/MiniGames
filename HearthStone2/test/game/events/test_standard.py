#! /usr/bin/python
# -*- coding: utf-8 -*-

import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))

from MyHearthStone.game.player import Player
from MyHearthStone.game import player_action as pa
from MyHearthStone.game.events import standard as std_e
from MyHearthStone.utils.game import Zone

from ..utils import ExpectedEntities, example_game, ExampleDecks

__author__ = 'fyabc'


class TestStdEvents(unittest.TestCase):
    test_decks = [None, None]
    expected_entities = ExpectedEntities
    game_start_events = [std_e.BeginOfGame, std_e.BeginOfTurn, std_e.DrawCard]

    @classmethod
    def setUpClass(cls):
        cls.test_decks = ExampleDecks

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.game = example_game()
        self.p0, self.p1 = self.game.players[self.game.current_player], self.game.players[1 - self.game.current_player]

    def tearDown(self):
        self.game.end_game()

    def _assertEventType(self, event_types):
        self.assertListEqual(event_types, [type(e) for e in self.game.event_history])

    def testGameStartEvents(self):
        """Test if game start events are expected."""
        self._assertEventType(self.game_start_events)
