#! /usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from MyHearthStone.game.deck import Deck
from MyHearthStone.network.lan_client import start_client
from MyHearthStone.utils.package_io import search_by_name
from MyHearthStone.utils.message import setup_logging

__author__ = 'fyabc'


def main():
    import random

    setup_logging(file=None, scr_log=True)

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

