#! /usr/bin/python
# -*- coding: utf-8 -*-

import os
import time
import argparse
import tkinter as tk

from .gui_tools.tkgui.game_window import GameWindow
from .core import Game
from .utils.debug import *
from .utils.config import DefaultGameFile, AppDataPath
from .utils.io_utils import make_directories

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
        const=os.path.join(AppDataPath.user_log_dir, 'HS_log_{}.txt'.format(time.strftime('%y_%m_%d_%H_%M_%S'))),
        help='The logging filename (default is do not logging, if filename of -l not given, '
             'it will be put in the log directory of AppData)')
    parser.add_argument(
        '-d', '--debug', metavar='level', dest='debug_level', type=str,
        choices=['debug', 'verbose', 'info', 'common', 'warning', 'error'], default='common',
        help='The debug level, default is "common"')

    return parser


def main():
    make_directories()

    parser = get_parser()
    options = parser.parse_args()

    set_debug_level(eval('LEVEL_{}'.format(options.debug_level.upper())))

    print('This is the GUI main script of the package HearthStone!')

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
