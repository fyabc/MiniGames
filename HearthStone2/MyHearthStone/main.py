#! /usr/bin/python
# -*- coding: utf-8 -*-

from .game.core import Game
from .game.deck import Deck
from .game import player_action

__author__ = 'fyabc'


def main():
    game = Game()
    decks = [
        Deck(0, [0]),
        Deck(1, [0, 0])
    ]

    game.start_game(decks)

    actions = [
        player_action.TurnEnd(game),
        player_action.TurnEnd(game),
        player_action.TurnEnd(game),
        player_action.PlaySpell(game, game.hands[0][0], None),
    ]

    for action in actions:
        print('*' * 80)
        game.run_player_action(action)

    game.show_details()


if __name__ == '__main__':
    main()
