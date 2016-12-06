#! /usr/bin/python
# -*- coding: utf-8 -*-

import tkinter as tk
from HearthStone.gui_tools import GameWindow
from HearthStone.core import Game

__author__ = 'fyabc'


def _test():
    root = tk.Tk(className='HearthStone')
    root.geometry("1050x600")

    game = Game('./data/example_game.json')

    app = GameWindow(game, root)

    app.mainloop()


if __name__ == '__main__':
    _test()
