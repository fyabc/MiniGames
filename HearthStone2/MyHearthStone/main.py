#! /usr/bin/python
# -*- coding: utf-8 -*-

from .game.core import Game
from .utils.package_io import all_cards

__author__ = 'fyabc'


def main():
    AllCards = all_cards()

    game = Game()

    from .game.player_action import TurnEnd

    game.run_player_action(TurnEnd(game, 0))

    print(AllCards)


if __name__ == '__main__':
    main()
