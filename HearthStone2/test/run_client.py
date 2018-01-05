#! /usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from MyHearthStone.game.deck import Deck
from MyHearthStone.network.lan_client import start_client
from MyHearthStone.utils.package_io import search_by_name
from MyHearthStone.utils.message import set_debug_level, LEVEL_DEBUG

__author__ = 'fyabc'


def main():
    import random

    set_debug_level(LEVEL_DEBUG)

    deck = Deck(
        0,
        [search_by_name(n) for n in [
            '工程师学徒',
            '工程师学徒',
            '工程师学徒',
            '工程师学徒',
            '工程师学徒',
            '工程师学徒',
        ]]
    )
    start_client(('localhost', 20000), 'user{}'.format(random.randint(1, 10)), deck.to_code())


if __name__ == '__main__':
    main()

