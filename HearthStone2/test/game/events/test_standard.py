#! /usr/bin/python
# -*- coding: utf-8 -*-

import unittest

from MyHearthStone.game.events import standard as std_e

from HearthStone2.test.test_utils.example import ExpectedEntities, example_game, ExampleDecks

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
