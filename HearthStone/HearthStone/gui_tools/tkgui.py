#! /usr/bin/python
# -*- coding: utf-8 -*-

import tkinter as tk

__author__ = 'fyabc'


class GameWindow(tk.Frame):
    def __init__(self, game, master=None):
        super(GameWindow, self).__init__(master=master)
        self.pack(fill=tk.BOTH)

        self.game = game

        ########
        # Menu #
        ########

        self.menu_bar = tk.Menu(self.master)
        self.master.config(menu=self.menu_bar)

        # All cascade menus.
        self.cascade_menus = {
            'Game': tk.Menu(self.menu_bar),
            'Help': tk.Menu(self.menu_bar),
        }

        self.menu_bar.add_cascade(label='Game', menu=self.cascade_menus['Game'])
        self.menu_bar.add_cascade(label='Help', menu=self.cascade_menus['Help'])
        self.menu_bar.add_command(label='Quit', command=self.quit)

        # Window Layouts.

        # Left: History layout.

        # Center: Game board layout.

        # Right: Deck layout.


__all__ = [
    'GameWindow',
]
