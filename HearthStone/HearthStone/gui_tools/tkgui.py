#! /usr/bin/python
# -*- coding: utf-8 -*-

from functools import wraps
from tkinter import *
from tkinter.ttk import *

from ..game_events import GameBegin, GameEnd, TurnEnd, SummonMinion
from ..cli_tool import show_card, show_minion

__author__ = 'fyabc'


class GameWindow(Frame):
    """The Tk game window.

    """

    # [NOTE] Some rules of the variable's name in the layout:
    # There are two players in the game. I am Player 0, opponent is Player 1.
    # `self.deck_frame_0`, `self.deck_frame_1`

    # [NOTE] Selection states:
    #   0 = not anything selected
    #   n = n objects selected

    def __init__(self, game, master=None):
        super(GameWindow, self).__init__(master=master, borderwidth=30)
        self.pack(fill=BOTH)

        self.game = game

        self.selection_state = 0

        ########
        # Menu #
        ########

        self.menu_bar = Menu(self.master)
        self.master.config(menu=self.menu_bar)

        # All cascade menus.
        self.cascade_menus = {
            'Game': Menu(self.menu_bar),
            'Help': Menu(self.menu_bar),
        }

        self.menu_bar.add_cascade(label='Game', menu=self.cascade_menus['Game'])
        self.menu_bar.add_command(label='Game Begin', command=self.game_begin)
        self.menu_bar.add_command(label='Turn End', command=self.turn_end)
        self.menu_bar.add_command(label='Refresh', command=self.refresh_window)
        self.menu_bar.add_cascade(label='Help', menu=self.cascade_menus['Help'])
        self.menu_bar.add_command(label='Quit', command=self.quit)

        ###############################
        # Window Layout.              #
        #                             #
        #   -----------------------   #
        #   |    |   .   .   |    |   #
        #   -----------------------   #
        #   |    |   .   .   |    |   #
        #   -----------------------   #
        #                             #
        ###############################

        ########################
        # Left: History frame. #
        ########################
        self.history_frame = Frame(self, borderwidth=10)
        self.history_frame.grid(row=0, column=0, columnspan=2)

        #############################
        # Center: Game board frame. #
        #############################
        self.board_frame = Frame(self, borderwidth=10)
        self.board_frame.grid(row=0, column=1, rowspan=8, columnspan=2)

        self.minion_button = Button(self.board_frame, text='Minion 1\nMinion 2')
        self.minion_button.pack()

        ######################
        # Right: Deck frame. #
        ######################
        self.deck_number = [IntVar(self, 0), IntVar(self, 0)]

        # Labels of deck numbers.
        self.deck_label_0 = Label(
            self,
            borderwidth=10,
            textvariable=self.deck_number[0]
        )
        self.deck_label_0.grid(row=0, column=9)

        self.deck_label_1 = Label(
            self,
            borderwidth=10,
            textvariable=self.deck_number[1]
        )
        self.deck_label_1.grid(row=1, column=9)

        ############################
        # Some initial operations. #
        ############################

        self.refresh_window()

    def refresh_window(self):
        """Refresh all elements of the game window."""

        self.refresh_minions()
        self.refresh_deck()

    def refresh_minions(self):
        for element in self.board_frame.winfo_children():
            element.destroy()

        for i in (0, 1):
            player = self.game.players[i]

            # Refresh desk.
            for n, card in enumerate(player.desk):
                minion_button = Button(self.board_frame, text=show_minion(card))
                minion_button.grid(row=2 if i == 0 else 1, column=n)

            # Refresh hand.
            for n, card in enumerate(player.hand):
                minion_button = Button(
                    self.board_frame,
                    text=show_card(card),
                    command=lambda: self.on_hand_click(n),
                )
                minion_button.grid(row=3 if i == 0 else 0, column=n)

    def refresh_deck(self):
        for i in (0, 1):
            self.deck_number[i].set(self.game.players[i].deck_number)

    def _add_select(self):
        self.selection_state += 1

    def _clear_select(self):
        self.selection_state = 0

    # Some user operations.
    def game_begin(self):
        self.game.restart_game()
        self.game.dispatch_event_quick(GameBegin)
        self.refresh_window()

    def turn_end(self):
        self.game.dispatch_event_quick(TurnEnd)
        self.refresh_window()

    def on_hand_click(self, index):
        print('Click hand!', n)


__all__ = [
    'GameWindow',
]
