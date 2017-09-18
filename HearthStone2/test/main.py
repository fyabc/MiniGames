#! /usr/bin/python
# -*- encoding: utf-8 -*-

"""Quick test changes of code, without install."""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from MyHearthStone.utils.message import set_debug_level, LEVEL_INFO, LEVEL_DEBUG
from MyHearthStone.game.core import Game
from MyHearthStone.game.deck import Deck
from MyHearthStone.game import player_action

__author__ = 'fyabc'


def play_inplace(action_type, game, player_id, index, target=None):
    return action_type(game, game.hands[player_id][index], player_id, target)


def main():
    game = Game()
    decks = [
        Deck(0, [0, 20004]),
        Deck(1, [1, 0])
    ]

    game.start_game(decks)

    actions = [
        # 0
        player_action.TurnEnd(game),
        # 1
        player_action.TurnEnd(game),
        # 0
        (player_action.PlaySpell, game, 0, 0),
        player_action.TurnEnd(game),
        # 1
        (player_action.PlayMinion, game, 1, 0),
        player_action.TurnEnd(game),
        # 0
    ]

    game.show_details()
    for action in actions:
        print('*' * 80)
        if isinstance(action, tuple):
            action = play_inplace(*action)
        game.run_player_action(action)
        game.show_details()


if __name__ == '__main__':
    set_debug_level(LEVEL_DEBUG)

    main()
