#! /usr/bin/python
# -*- coding: utf-8 -*-

import tkinter as tk

__author__ = 'fyabc'


class GameWindow(tk.Frame):
    def __init__(self, game, master=None):
        super(GameWindow, self).__init__(master=master, borderwidth=30)
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

        ##################
        # Window Layout. #
        ##################

        ########################
        # Left: History frame. #
        ########################
        self.history_frame = tk.Frame(self, borderwidth=0)
        self.history_frame.pack(side=tk.LEFT)

        #############################
        # Center: Game board frame. #
        #############################
        self.board_frame = tk.Frame(self, borderwidth=0)
        self.board_frame.pack(side=tk.LEFT)

        ######################
        # Right: Deck frame. #
        ######################
        self.deck_frame = tk.Frame(self, borderwidth=0)
        self.deck_frame.pack(side=tk.RIGHT)

        self.deck_labels = [
            tk.Label(self.deck_frame,
                     text='Hello'),
            tk.Label(self.deck_frame,
                     text='World'),
        ]

        self.deck_labels[0].pack(
            side=tk.TOP,
            fill=tk.BOTH,
            expand=True,
        )
        self.deck_labels[1].pack(
            side=tk.BOTTOM,
            fill=tk.BOTH,
            expand=True,
        )


__all__ = [
    'GameWindow',
]
