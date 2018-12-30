#! /usr/bin/python
# -*- coding: utf-8 -*-

import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))

from MyHearthStone.game import player_action as pa
from MyHearthStone.game.events import standard as std_e
from MyHearthStone.utils.game import Zone

from .utils import *

__author__ = 'fyabc'

# Game Start Events.
GSE = [std_e.BeginOfGame, std_e.BeginOfTurn, std_e.DrawCard]


class TestPlayerActions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_decks = ExampleDecks

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.game = example_game()
        self.p0, self.p1 = self.game.get_player(self.game.current_player), \
            self.game.get_player(1 - self.game.current_player)

    def tearDown(self):
        self.game.end_game()

    def _printEventHistory(self):
        print([e.__class__.__name__ for e in self.game.event_history])

    def _assertEventType(self, event_types):
        self.assertListEqual(event_types, [type(e) for e in self.game.event_history])

    def _prepare_card(self, card_id, player_id=None):
        """Prepare enough mana and generate target card into hand directly."""
        if player_id is None:
            player = self.p0
        else:
            player = self.game.get_player(player_id)
        player.add_mana(10, 'T')
        card, _ = player.generate(Zone.Hand, 'last', card_id)
        return card

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

        self._assertEventType(GSE + [std_e.EndOfTurn, std_e.BeginOfTurn, std_e.DrawCard])

    def testConcede(self):
        """Test the concede player action."""
        current_player = self.game.current_player
        self.game.run_player_action(pa.Concede(self.game))

        self._assertEventType(GSE + [std_e.HeroDeath])
        self.assertEqual(self.game.event_history[-1].owner.player_id, current_player)

    def testPlaySpell(self):
        """Test the play spell action."""

        spell = self._prepare_card(C30007)  # 火球术

        self.assertEqual(spell.id, C30007)
        self.game.run_player_action(pa.PlaySpell(self.game, spell, self.p1.hero))

        self._assertEventType(GSE + [
            std_e.OnPlaySpell, std_e.SpellBenderPhase, std_e.SpellText, std_e.Damage, std_e.AfterSpell,
        ])

    def testPlayWeapon(self):
        C90008 = '90008'    # 炽炎战斧
        weapon = self._prepare_card(C90008)

        self.game.run_player_action(pa.PlayWeapon(self.game, weapon, None))

        self._assertEventType(GSE + [
            std_e.OnPlayWeapon, std_e.EquipWeapon, std_e.AfterPlayWeapon,
        ])

    def testPlayMinion(self):
        minion = self._prepare_card(C10000)     # 埃隆巴克保护者

        self.game.run_player_action(pa.PlayMinion(self.game, minion, 0, None))

        self._assertEventType(GSE + [
            std_e.OnPlayMinion, std_e.Summon, std_e.BattlecryPhase, std_e.AfterPlayMinion, std_e.AfterSummon,
        ])

    def testUseHeroPower(self):
        hp = self.game.get_player(self.game.current_player).hero_power  # 稳固射击
        self.assertEqual(hp.id, 1)
        self.p0.add_mana(10, 'T')

        self.game.run_player_action(pa.UseHeroPower(self.game, None, self.game.current_player))

        self.assertEqual(self.game.get_hero(1 - self.game.current_player).health, 28)
        assert_events1 = GSE + [
            std_e.HeroPowerPhase, std_e.Damage, std_e.InspirePhase,
        ]
        self._assertEventType(assert_events1)

        expected_events2 = self._turnEnds(1)

        hp = self.game.get_player(self.game.current_player).hero_power  # 火焰冲击
        self.assertEqual(hp.id, 2)
        self.p1.add_mana(10, 'T')

        self.game.run_player_action(pa.UseHeroPower(
            self.game, self.game.get_hero(1 - self.game.current_player), self.game.current_player))

        self.assertEqual(self.game.get_hero(1 - self.game.current_player).health, 29)
        self._assertEventType(assert_events1 + expected_events2 + [
            std_e.HeroPowerPhase, std_e.Damage, std_e.InspirePhase,
        ])

    def testToAttack(self):
        # TODO
        pass


class TestReplaceStartCard(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_decks = ExampleDecks

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.game = example_game(replace_start_card=False)
        self.p0, self.p1 = self.game.get_player(0), self.game.get_player(1)

    def _get_hand(self, player_id):
        return id_list(self.game.get_zone(Zone.Hand, player_id))

    def testReplaceStartCard(self):
        self.assertListEqual(self._get_hand(0), [C30007, C6, C11, C11])
        self.assertListEqual(self._get_hand(1), [C11, C30007, C11])

        self.game.run_player_action(pa.ReplaceStartCard(self.game, 0, [2, 3]))
        self.game.run_player_action(pa.ReplaceStartCard(self.game, 1, [1, 2]))

        self.assertListEqual(self._get_hand(0), [C30007, C6, C30007, C6, Coin])
        self.assertListEqual(self._get_hand(1), [C11, C30007, C10000, C6])

    def testInvalidReplace(self):
        with self.assertRaises(IndexError):
            # The exception will only be raised after both two replace actions.
            self.game.run_player_action(pa.ReplaceStartCard(self.game, 0, [2, 3]))
            self.game.run_player_action(pa.ReplaceStartCard(self.game, 1, [1, 3]))
