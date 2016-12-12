#! /usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import tkinter as tk

from .gui_tools.tkgui import GameWindow
from .core import Game

__author__ = 'fyabc'


def get_parser():
    parser = argparse.ArgumentParser(description='The Python implementation of HearthStone')

    return parser


def main():
    parser = get_parser()

    print('This is the GUI main script of the package HearthStone!')

    # options = parser.parse_args()

    root = tk.Tk(className='HearthStone')
    root.geometry("1050x600")

    game = Game('C:/Users/v-yanfa/PycharmProjects/MiniGames/HearthStone/test/data/example_game.json',
                logging_filename=None)

    app = GameWindow(game, root)

    app.mainloop()


if __name__ == '__main__':
    main()
