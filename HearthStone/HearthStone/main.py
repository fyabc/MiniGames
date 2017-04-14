#! /usr/bin/python
# -*- coding: utf-8 -*-

import os
import time
import argparse
import tkinter as tk

from .gui_tools.tkgui.game_window import GameWindow
from .core import Game
from .utils.config import DefaultGameFile

__author__ = 'fyabc'


def get_parser():
    parser = argparse.ArgumentParser(description='The Python implementation of HearthStone')
    parser.add_argument(
        '-s', '--size', metavar='axb', dest='size', type=str, default='1050x600',
        help='The window size of the game, format is "axb" (default is "1050x600")'
    )
    parser.add_argument(
        '-g', '--game', metavar='filename', dest='game', type=str, default=DefaultGameFile,
        help='The game file to be load (default is an example game file)')
    parser.add_argument(
        '-l', '--log', nargs='?', metavar='log_filename', dest='log', type=str, default=None,
        const=os.path.join(os.path.expanduser('~'), 'HS_log_{}.txt'.format(time.strftime('%y_%m_%d_%H_%M_%S'))),
        help='The logging filename (default is do not logging, if filename of -l not given, '
             'it will be put in your home directory.)')

    return parser


def main():
    parser = get_parser()

    print('This is the GUI main script of the package HearthStone!')

    options = parser.parse_args()

    root = tk.Tk(className='HearthStone')
    root.geometry(options.size)

    game = Game(
        game_filename=options.game,
        logging_filename=options.log,
    )

    app = GameWindow(game, root)

    app.mainloop()


if __name__ == '__main__':
    main()
