#! /usr/bin/python
# -*- coding: utf-8 -*-

import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))

from MyHearthStone.game import player_action as pa
from MyHearthStone.game.events import standard as std_e
from MyHearthStone.utils.game import Zone

from .utils import ExpectedEntities, example_game, ExampleDecks

__author__ = 'fyabc'


class TestPlayerActions(unittest.TestCase):
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

    def _printEventHistory(self):
        print([e.__class__.__name__ for e in self.game.event_history])

    def _assertEventType(self, event_types):
        self.assertListEqual(event_types, [type(e) for e in self.game.event_history])

    def _turnEnds(self, n):
        """Run many turn-ends player actions.

        [NOTE]: The return expected event list is correct only when not taking fatigue damage.
        """
        expected_events = []
        for _ in range(n):
            self.game.run_player_action(pa.TurnEnd(self.game))
            expected_events.extend([std_e.EndOfTurn, std_e.BeginOfTurn, std_e.DrawCard])
        return expected_events

    # Player action tests.

    def testTurnEnd(self):
        """Test the turn end player action."""
        player_before = self.game.current_player
        self.game.run_player_action(pa.TurnEnd(self.game))
        self.assertNotEqual(player_before, self.game.current_player)

        self._assertEventType(self.game_start_events + [std_e.EndOfTurn, std_e.BeginOfTurn, std_e.DrawCard])

    def testConcede(self):
        """Test the concede player action."""
        current_player = self.game.current_player
        self.game.run_player_action(pa.Concede(self.game))

        self._assertEventType(self.game_start_events + [std_e.HeroDeath])
        self.assertEqual(self.game.event_history[-1].owner.player_id, current_player)

    def testPlaySpell(self):
        """Test the play spell action."""

        expected_events = self._turnEnds(3 * 2)

        # Current mana == 4, hand[1] == 火球术
        self.assertEqual(self.p0.displayed_mana(), 4)

        spell = self.p0.get_zone(Zone.Hand)[1]
        self.assertEqual(spell.id, "30007")
        self.game.run_player_action(pa.PlaySpell(self.game, spell, self.p1.hero))

        self._assertEventType(self.game_start_events + expected_events + [
            std_e.OnPlaySpell, std_e.SpellBenderPhase, std_e.SpellText, std_e.Damage, std_e.AfterSpell,
        ])

    # TODO: Generate new cards directly to run tests.

    def testUseHeroPower(self):
        expected_events = self._turnEnds(2 * 1)

        # Hero power == 稳固射击
        hp = self.game.get_player(self.game.current_player).hero_power
        self.assertEqual(hp.id, 1)

        self.game.run_player_action(pa.UseHeroPower(self.game, None, self.game.current_player))

        self.assertEqual(self.game.get_hero(1 - self.game.current_player).health, 28)
        assert_events1 = self.game_start_events + expected_events + [
            std_e.HeroPowerPhase, std_e.Damage, std_e.InspirePhase,
        ]
        self._assertEventType(assert_events1)

        expected_events2 = self._turnEnds(1)

        # Hero power == 火焰冲击
        hp = self.game.get_player(self.game.current_player).hero_power
        self.assertEqual(hp.id, 2)

        # TODO
        self.game.run_player_action(pa.UseHeroPower(
            self.game, self.game.get_hero(1 - self.game.current_player), self.game.current_player))

        self.assertEqual(self.game.get_hero(1 - self.game.current_player).health, 29)
        self._assertEventType(assert_events1 + expected_events2 + [
            std_e.HeroPowerPhase, std_e.Damage, std_e.InspirePhase,
        ])
