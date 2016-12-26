#! /usr/bin/python
# -*- coding: utf-8 -*-

import tkinter as tk
from HearthStone.gui_tools import GameWindow
from HearthStone.core import Game
from HearthStone.utils.debug_utils import set_debug_level, LEVEL_DEBUG

__author__ = 'fyabc'


def _test():
    set_debug_level(LEVEL_DEBUG)

    root = tk.Tk(className='HearthStone')
    root.geometry("1140x600")

    game = Game('./data/example_game.json')

    app = GameWindow(game, root)

    app.mainloop()


if __name__ == '__main__':
    _test()
