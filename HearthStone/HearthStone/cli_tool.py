#! /usr/bin/python
# -*- coding: utf-8 -*-

"""Some tools for command line interface.

Try to run HearthStone on command line more effectively.
"""

import sys
import os
import shutil

from .utils import verbose, Config
from .core import Game

__author__ = 'fyabc'

CLIConfig = Config['CLI']

WIN32 = sys.platform == 'win32'

windowWidth = Config['CLI']['windowWidth']


# todo: remove the type signature in future.


def clear_screen():
    if WIN32:
        os.system('cls')
    else:
        os.system('clear')


def simple_show_board(game: Game):
    p0, p1 = game.players

    verbose('''\
        {}
        | P0: HP={} Crystal={}/{}
        | Hand={}
        | Deck={}
        | Desk={}
        | P1: HP={} Crystal={}/{}
        | Hand={}
        | Deck={}
        | Desk={}
        {}
    '''.format(
        'Game Status'.center(windowWidth, Config['CLI']['charShowBegin']),
        p0.health, p0.remain_crystal, p0.total_crystal,
        p0.hand, p0.deck, p0.desk,
        p1.health, p1.remain_crystal, p1.total_crystal,
        p1.hand, p1.deck, p1.desk,
        'Status End'.center(windowWidth, Config['CLI']['charShowEnd']),
    ))


def show_board(game: Game):
    """Show the board of the game.

    :param game: The game to be show.
    :return: None
    """

    '''The game board is like this:

    T = Taunt
    S = Stealth
    D = Divine Shield
    C = Charge
    (W = Windfury, but not shown in the card)

                    ---------
    Cost ---------> |2  #100| <-- Card ID
    Can attack? --> |*      |
    Attributes ---> |T S D C|
    Attack -------> |3     2| <-- Health
                    ---------

            ================================================
            |   P1            [6]                   |      |
            |---------------------------------------|      |
            |              |2    #1|                |      |
            |              |*      |                | [26] |
            |              |T S D C|                |      |
            |              |3     2|                |      |
            |---------------------------------------|------|
            |                                       |      |
            |                                       |      |
            |                                       | [25] |
            |                                       |      |
            |---------------------------------------|      |
            | * P0                                  |      |
            ================================================
    '''

    p0, p1 = game.players

    columns, lines = shutil.get_terminal_size()


__all__ = [
    'CLIConfig',
    'clear_screen',
    'simple_show_board',
    'show_board',
]
