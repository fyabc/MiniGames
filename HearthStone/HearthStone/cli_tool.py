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
from .game_entities.card import Card, Minion, Spell, Weapon

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


def align_line(left_line, right_line, width=120, fill=' ', sep=' '):
    assert len(fill) == 1, 'Length of fill char must be 1'
    assert len(sep) == 1, 'Length of separate char must be 1'

    if not isinstance(left_line, (list, tuple)):
        left_line = [left_line]
    if not isinstance(right_line, (list, tuple)):
        right_line = [right_line]

    return '{}{}{}{}'.format(
        sep.join(str(e) for e in left_line),
        fill,
        fill * (width - len(left_line) - len(right_line) - 1),
        sep.join(str(e) for e in right_line),
    )


def show_card(card, width=7):
    if isinstance(card, Minion):
        return show_minion(card, width)
    # todo: change to show_spell & show_weapon
    elif isinstance(card, Spell):
        return show_spell(card, width)
    elif isinstance(card, Weapon):
        return show_weapon(card, width)


def show_minion(minion: Minion, width=7, border=False):
    b = '|' if border else ''

    return '''\
{}{}{}
{}{}{}
{}{}{}
{}{}{}
{}{}{}
'''.format(
        b, minion.data['name'].center(width), b,
        b, align_line(minion.cost, '#{}'.format(minion.data['id']), width), b,
        b, align_line('*' if minion.remain_attack_number > 0 else [], [], width), b,
        b, '{} {} {} {}'.format(
            'T' if minion.taunt else ' ',
            'S' if minion.stealth else ' ',
            'D' if minion.divine_shield else ' ',
            'C' if minion.charge else ' ',
        ), b,
        b, align_line(minion.attack, minion.health, width), b,
    )


def show_spell(spell: Spell, width=7):
    pass


def show_weapon(weapon: Weapon, width=7):
    pass


__all__ = [
    'CLIConfig',
    'clear_screen',
    'simple_show_board',
    'show_board',
    'align_line',
    'show_card',
    'show_minion',
]
