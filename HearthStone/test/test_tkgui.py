#! /usr/bin/python
# -*- coding: utf-8 -*-

import os
import time
import tkinter as tk

from HearthStone.gui_tools.tkgui.game_window import GameWindow
from HearthStone.core import Game
from HearthStone.utils.debug import set_debug_level, LEVEL_DEBUG

__author__ = 'fyabc'


def _test():
    set_debug_level(LEVEL_DEBUG)

    logging_filename = '{}/PycharmProjects/MiniGames/HearthStone/test/logs/log_engine_{}.txt'.format(
        os.path.expanduser('~'),
        time.strftime('%y_%m_%d_%H_%M_%S')
    )

    root = tk.Tk(className='HearthStone')
    root.geometry("1140x600")

    game = Game('./data/example_game.json', logging_filename=logging_filename)

    app = GameWindow(game, root)

    app.mainloop()


if __name__ == '__main__':
    _test()
