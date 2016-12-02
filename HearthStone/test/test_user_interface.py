#! /usr/bin/python
# -*- encoding: utf-8 -*-

from HearthStone.core import Game
from HearthStone.user_interface import GameUserInterface
from HearthStone.game_exception import GameEndException
from HearthStone.utils import set_debug_level, LEVEL_DEBUG, error

__author__ = 'fyabc'


# CLI methods.
Commands = {
    'show': 'show',
    's': 'show',

    'clear_screen': 'clear_screen',
    'clear': 'clear_screen',
    'cls': 'clear_screen',

    'game_begin': 'game_begin',
    'gb': 'game_begin',
    '^': 'game_begin',

    'game_end': 'game_end',
    'ge': 'game_end',
    '$': 'game_end',

    'turn_end': 'turn_end',
    'te': 'turn_end',
    '#': 'turn_end',

    'play_card': 'try_play_card',
    'play': 'try_play_card',
    'p': 'try_play_card',

    'attack': 'try_attack',
    'a': 'try_attack',
}


def take_operation(ui, op_name, *args):
    command = Commands.get(op_name, None)

    if command is None:
        error('Unknown operation: {}'.format(op_name))
        return

    exec('ui.{}({})'.format(command, ','.join(args)))


def _test():
    game = Game('./data/example_game.json')

    set_debug_level(LEVEL_DEBUG)

    ui = GameUserInterface(game)

    try:
        while True:
            words = input('operation> ').split()

            if len(words) == 0:
                continue

            take_operation(ui, *words)
    except GameEndException as e:
        print(e.message())


if __name__ == '__main__':
    _test()
