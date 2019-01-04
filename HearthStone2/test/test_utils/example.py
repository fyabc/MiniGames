#! /usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import random

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))

from MyHearthStone.game.core import Game
from MyHearthStone.game.deck import Deck
from MyHearthStone.game import player_action as pa
from MyHearthStone.game.events import standard as std_e
from MyHearthStone.utils.game import Klass, Zone

__author__ = 'fyabc'

Seed = 1234

C6 = '6'            # 工程师学徒
C11 = '11'          # 淡水鳄
C10000 = '10000'    # 埃隆巴克保护者
C30007 = '30007'    # 火球术
Coin = '43'         # 幸运币

ExampleDecks = [
    Deck(klass=Klass.Str2Idx['Mage'], card_id_list=[
        C6, C6, C6, C6,
        C11, C11, C11, C11,
        C10000, C10000, C10000, C10000,
        C30007, C30007, C30007, C30007,
    ], name='Test Mage'),
    Deck(klass=Klass.Str2Idx['Hunter'], card_id_list=[
        C6, C6, C6, C6,
        C11, C11, C11, C11,
        C10000, C10000, C10000, C10000,
        C30007, C30007, C30007, C30007,
    ], name='Test Hunter'),
]

ExpectedEntities = [
    {
        Zone.Deck: [C6, C6, C10000, C30007, C11, C10000, C30007, C10000, C10000, C11, C6, C30007],
        Zone.Hand: [C30007, C6, C11, C11, Coin],
        Zone.Play: [],
        Zone.Secret: [],
        Zone.Graveyard: [],
        Zone.Weapon: [],
        Zone.Hero: [2],
        Zone.HeroPower: [2],
    },
    {
        Zone.Deck: [C11, C10000, C6, C30007, C10000, C30007, C11, C6, C10000, C30007, C10000, C6],
        Zone.Hand: [C11, C30007, C11, C6],
        Zone.Play: [],
        Zone.Secret: [],
        Zone.Graveyard: [],
        Zone.Weapon: [],
        Zone.Hero: [1],
        Zone.HeroPower: [1],
    },
]

# Game Start Events.
GSE = [std_e.BeginOfGame, std_e.BeginOfTurn, std_e.DrawCard]


def example_game(decks=None, replace_start_card=True):
    decks = ExampleDecks if decks is None else decks

    random.seed(Seed)

    game = Game()
    game.start_game(decks, mode='standard')
    if replace_start_card:
        game.run_player_action(pa.ReplaceStartCard(game, 0, []))
        game.run_player_action(pa.ReplaceStartCard(game, 1, []))
    return game


def id_list(zone):
    return [e.id for e in zone]


__all__ = [
    'Seed',
    'C6', 'C11', 'C10000', 'C30007', 'Coin',
    'ExampleDecks', 'ExpectedEntities', 'GSE',
    'example_game',
    'id_list',
]
