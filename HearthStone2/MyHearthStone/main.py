#! /usr/bin/python
# -*- coding: utf-8 -*-

from .game.core import Game
from .game.deck import Deck
from .utils.package_io import all_cards, all_heroes

__author__ = 'fyabc'


def main():
    AllCards = all_cards()
    AllHeroes = all_heroes()

    print(AllCards, AllHeroes)

    game = Game()
    decks = [
        Deck(0, [0]),
        Deck(1, [0, 0])
    ]

    game.start_game(decks)

    from .game.player_action import TurnEnd

    actions = [
        TurnEnd(game),
    ]

    for action in actions:
        game.run_player_action(action)


if __name__ == '__main__':
    main()
