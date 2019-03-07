#! /usr/bin/python
# -*- coding: utf-8 -*-

import unittest

from ..test_utils.example import ExampleDecks, ExpectedEntities, example_game

from MyHearthStone.game.player import Player
from MyHearthStone.game import player_action as pa
from MyHearthStone.game.events import standard as std_e
from MyHearthStone.utils.game import Zone

__author__ = 'fyabc'


class TestCore(unittest.TestCase):
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

    def _print_zones(self):
        for player_id in 0, 1:
            for zone, z_name in Zone.Idx2Str.items():
                if zone in (Zone.Invalid, Zone.SetAside, Zone.RFG):
                    continue
                print('{} {}'.format(player_id, z_name),
                      [e.id if e is not None else None for e in self.game.get_zone(zone, player_id)])

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
            for zone in Zone.Idx2Str:
                if zone in (Zone.Invalid, Zone.SetAside, Zone.RFG):
                    continue
                zone_entities = self.game.get_zone(zone, player_id)
                for entity in zone_entities:
                    if entity is None:
                        continue
                    self.assertEqual(entity.zone, zone, 'Entity {} in zone {} has an incorrect zone {}'.format(
                        entity, Zone.repr_zp(zone, player_id), Zone.repr_zp(entity.zone, entity.player_id)))

    # Game basic tests.

    def testBasic(self):
        """Some basic tests."""
        self.assertEqual(self.game.state, self.game.GameState.Main, 'Game is not in main state')
        self.assertIsInstance(self.p0, Player, 'Offensive player is not successfully created')
        self.assertIsInstance(self.p1, Player, 'Defensive player is not successfully created')

    def testStartZones(self):
        """Test length of some start zones."""
        self._assertExpectedZones()

    def testZones(self):
        """Test the correctness of entity zones in play."""
        self._assertZoneAttr()
        self.game.run_player_action(pa.TurnEnd(self.game))
        self._assertZoneAttr()
        self.game.run_player_action(pa.Concede(self.game))
        self._assertZoneAttr()

    def _assertManas(self, player, m, u, t, o, on, d):
        self.assertEqual(player.max_mana, m, 'Max mana not equal')
        self.assertEqual(player.used_mana, u, 'Used mana not equal')
        self.assertEqual(player.temp_mana, t, 'Temp mana not equal')
        self.assertEqual(player.overload, o, 'Overload mana not equal')
        self.assertEqual(player.overload_next, on, 'Overload next mana not equal')
        self.assertEqual(player.displayed_mana(), d, 'Displayed mana not equal')

    def testTempMana(self):
        game = self.game
        player = game.get_player(0)
        self._assertManas(player, 0, 0, 0, 0, 0, 0)
        player.add_mana(4, 'M')
        self._assertManas(player, 4, 4, 0, 0, 0, 0)
        player.add_mana(12, 'T')
        self._assertManas(player, 4, 4, 10, 0, 0, 10)
        player.spend_mana(7)
        self._assertManas(player, 4, 4, 3, 0, 0, 3)
        player.add_mana(6, 'T')
        self._assertManas(player, 4, 4, 9, 0, 0, 9)
