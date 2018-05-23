#! /usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import random

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))

from MyHearthStone.game.core import Game
from MyHearthStone.game.deck import Deck
from MyHearthStone.game import player_action as pa
from MyHearthStone.utils.game import Klass, Zone

__author__ = 'fyabc'

Seed = 1234

ExampleDecks = [
    Deck(klass=Klass.Str2Idx['Mage'], card_id_list=[
        "6", "6", "6", "6",
        "11", "11", "11", "11",
        "10000", "10000", "10000", "10000",
        "30007", "30007", "30007", "30007",
    ], name='Test Mage'),
    Deck(klass=Klass.Str2Idx['Hunter'], card_id_list=[
        "6", "6", "6", "6",
        "11", "11", "11", "11",
        "10000", "10000", "10000", "10000",
        "30007", "30007", "30007", "30007",
    ], name='Test Hunter'),
]

ExpectedEntities = [
    {
        Zone.Deck: ['6', '6', '10000', '30007', '11', '10000', '30007', '10000', '10000', '11', '6', '30007'],
        Zone.Hand: ['30007', '6', '11', '11', '43'],
        Zone.Play: [],
        Zone.Secret: [],
        Zone.Graveyard: [],
        Zone.Weapon: [],
        Zone.Hero: [2],
        Zone.HeroPower: [2],
    },
    {
        Zone.Deck: ['11', '10000', '6', '30007', '10000', '30007', '11', '6', '10000', '30007', '10000', '6'],
        Zone.Hand: ['11', '30007', '11', '6'],
        Zone.Play: [],
        Zone.Secret: [],
        Zone.Graveyard: [],
        Zone.Weapon: [],
        Zone.Hero: [1],
        Zone.HeroPower: [1],
    },
]


def example_game(decks=None):
    decks = ExampleDecks if decks is None else decks

    random.seed(Seed)

    game = Game()
    game.start_game(decks, mode='standard')
    game.run_player_action(pa.ReplaceStartCard(game, 0, []))
    game.run_player_action(pa.ReplaceStartCard(game, 1, []))
    return game
