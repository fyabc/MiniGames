#! /usr/bin/python
# -*- encoding: utf-8 -*-

"""Quick test changes of code, without install."""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# Load project config.
# [NOTE]: This must before the import of any other game modules.
from MyHearthStone.utils.constants import load_arg_config
load_arg_config({})

from MyHearthStone.utils.message import set_debug_level, LEVEL_INFO, LEVEL_DEBUG
from MyHearthStone.game.core import Game
from MyHearthStone.game.deck import Deck
from MyHearthStone.game import player_action
from MyHearthStone.utils.package_io import search_by_name

__author__ = 'fyabc'


class Runner:
    def run(self):
        pass


class PM(Runner):
    def __init__(self, game, index, loc, target, player_id=None):
        self.game = game
        self.player_id = player_id
        self.index = index
        self.loc = loc
        self.target = target

    def run(self):
        player_id = self.game.current_player if self.player_id is None else self.player_id
        return player_action.PlayMinion(self.game, self.game.hands[player_id][self.index],
                                        self.loc, self.target, player_id)


def main():
    game = Game()
    decks = [
        Deck(
            0,
            [search_by_name(n) for n in [
                '工程师学徒',
                '工程师学徒',
                '工程师学徒',
                '工程师学徒',
                '工程师学徒',
                '工程师学徒',
                '工程师学徒',
                '火球术',
                '火球术',
            ]]
        ),
        Deck(
            1,
            [search_by_name(n) for n in [
                '淡水鳄',
                '火球术',
                '淡水鳄',
                '淡水鳄',
                '淡水鳄',
                '淡水鳄',
                '淡水鳄',
                '淡水鳄',
                '淡水鳄',
            ]]
        ),
    ]

    start_game_iter = game.start_game(decks)
    try:
        next(start_game_iter)
        game.show_details()
        start_game_iter.send([[0], [1, 2]])
    except StopIteration:
        pass

    actions = [
        # 0
        player_action.TurnEnd(game),
        # 1
        player_action.TurnEnd(game),
        # 0
        PM(game, 1, 0, None),
        player_action.TurnEnd(game),
        # 1
        PM(game, 0, 0, None),
        player_action.TurnEnd(game),
        # 0
    ]

    game.show_details()
    for action in actions:
        print('*' * 80)
        if isinstance(action, Runner):
            action = action.run()
        game.run_player_action(action)
        game.show_details()


if __name__ == '__main__':
    set_debug_level(LEVEL_DEBUG)

    main()
