#! /usr/bin/python
# -*- coding: utf-8 -*-

from .game.core import Game
from .utils.package_io import all_cards

__author__ = 'fyabc'


def main():
    AllCards = all_cards()

    game = Game()

    print(AllCards)


if __name__ == '__main__':
    main()
