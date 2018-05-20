#! /usr/bin/python
# -*- coding: utf-8 -*-

import unittest
import sys
import os
import random

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))

from MyHearthStone.game.core import Game
from MyHearthStone.game.player import Player
from MyHearthStone.game.deck import Deck
from MyHearthStone.game import player_action as pa
from MyHearthStone.game.events import standard as std_e
from MyHearthStone.utils.game import Klass, Zone

__author__ = 'fyabc'


class TestCore(unittest.TestCase):
    test_decks = [None, None]

    game_start_events = [std_e.BeginOfGame, std_e.BeginOfTurn, std_e.DrawCard]

    seed = 1234

    expected_entities = [
        {
            Zone.Deck: ['6', '6', '10000', '30007', '11', '10000', '30007', '10000', '10000', '11', '6', '30007'],
            Zone.Hand: ['30007', '6', '11', '11', '43'],
            Zone.Play: [],
            Zone.Secret: [],
            Zone.Graveyard: [],
            Zone.Weapon: [None],
            Zone.Hero: [0],
            Zone.HeroPower: [0],
        },
        {
            Zone.Deck: ['11', '10000', '6', '30007', '10000', '30007', '11', '6', '10000', '30007', '10000', '6'],
            Zone.Hand: ['11', '30007', '11', '6'],
            Zone.Play: [],
            Zone.Secret: [],
            Zone.Graveyard: [],
            Zone.Weapon: [None],
            Zone.Hero: [1],
            Zone.HeroPower: [1],
        },
    ]

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
        # Set random seed to get reproducible behaviour.
        random.seed(self.seed)

        self.game = Game()
        self.game.start_game(self.test_decks, mode='standard')
        self.game.run_player_action(pa.ReplaceStartCard(self.game, 0, []))
        self.game.run_player_action(pa.ReplaceStartCard(self.game, 1, []))

        self.p0, self.p1 = self.game.players[self.game.current_player], self.game.players[1 - self.game.current_player]

    def tearDown(self):
        self.game.end_game()

    def _print_zones(self):
        for player_id in 0, 1:
            for zone, z_name in Zone.Idx2Str.items():
                if zone in (Zone.Invalid, Zone.SetAside, Zone.RFG):
                    continue
                print('{} {}'.format(player_id, z_name),
                      [e.id if e is not None else None for e in self.game.get_zone(zone, player_id)])

    def _assertEventType(self, event_types):
        self.assertListEqual(event_types, [type(e) for e in self.game.event_history])

    def _assertExpectedZones(self, expected_entities=None):
        expected_entities = self.expected_entities if expected_entities is None else expected_entities
        """Assert zones values as expected."""
        for player_id in 0, 1:
            for zone, z_name in Zone.Idx2Str.items():
                if zone in (Zone.Invalid, Zone.SetAside, Zone.RFG):
                    continue
                self.assertListEqual(
                    expected_entities[player_id][zone],
                    [e.id if e is not None else None for e in self.game.get_zone(zone, player_id)],
                    'Zone {!r} of player {} not as expected'.format(z_name, player_id),
                )

    def _assertZoneAttr(self):
        """Assert that the ``zone`` attribute of entities are correct."""
        for player_id in 0, 1:
            for zone, z_name in Zone.Idx2Str.items():
                if zone in (Zone.Invalid, Zone.SetAside, Zone.RFG):
                    continue
                zone_entities = self.game.get_zone(zone, player_id)
                for entity in zone_entities:
                    if entity is None:
                        continue
                    self.assertEqual(entity.zone, zone, 'Entity {} in zone {} has an incorrect zone {}'.format(
                        entity, z_name, Zone.Idx2Str[entity.zone]))

    # Game basic tests.

    def testBasic(self):
        """Some basic tests."""
        self.assertEqual(self.game.state, self.game.GameState.Main, 'Game is not in main state')
        self.assertIsInstance(self.p0, Player, 'Offensive player is not successfully created')
        self.assertIsInstance(self.p1, Player, 'Defensive player is not successfully created')

    def testStartZones(self):
        """Test length of some start zones."""
        self._assertExpectedZones()

    def testGameStartEvents(self):
        """Test if game start events are expected."""
        self._assertEventType(self.game_start_events)

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

    def testZones(self):
        """Test the correctness of entity zones in play."""
        # TODO: Test for more player actions.
        self._assertZoneAttr()
        self.game.run_player_action(pa.TurnEnd(self.game))
        self._assertZoneAttr()
        self.game.run_player_action(pa.Concede(self.game))
        self._assertZoneAttr()

    # TODO: Use ``_assertExpectedZones`` to run more tests.
