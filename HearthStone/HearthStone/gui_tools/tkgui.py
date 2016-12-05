#! /usr/bin/python
# -*- coding: utf-8 -*-

import tkinter as tk
import tkinter.ttk as ttk

from ..core import Game
from ..game_events import GameBegin, GameEnd, TurnEnd, SummonMinion
from ..cli_tool import show_card, show_minion

__author__ = 'fyabc'


class GameWindow(ttk.Frame):
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
        self.pack(fill=tk.BOTH)

        self.game = game

        self.selection_state = 0
        self.selections = []

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
        self.history_frame = ttk.Frame(self, borderwidth=10)
        self.history_frame.grid(row=0, column=0, columnspan=2)

        #############################
        # Center: Game board frame. #
        #############################
        board_frame_width = max(Game.MaxHandNumber, 2 * Game.MaxDeskNumber + 1)

        self.board_frame = ttk.Frame(self, borderwidth=10)
        self.board_frame.grid(row=0, column=1, rowspan=board_frame_width, columnspan=2)

        # todo: bind mouse press to select method
        self.board_frame.bind('<Button-1>', self.test_binding)

        # Fill the board with Buttons.
        # Buttons between minions should have smaller width.
        hand_card_pad = 0

        self.hand_card_buttons = [
            [ttk.Button(self.board_frame) for _ in range(Game.MaxHandNumber)],
            [ttk.Button(self.board_frame) for _ in range(Game.MaxHandNumber)],
        ]

        for i in (0, 1):
            for n, button in enumerate(self.hand_card_buttons[i]):
                button.grid(row=3 if i == 0 else 0, column=n, ipadx=hand_card_pad, ipady=hand_card_pad)

        self.desk_card_buttons = [
            [ttk.Button(self.board_frame) for _ in range(2 * Game.MaxDeskNumber + 1)],
            [ttk.Button(self.board_frame) for _ in range(2 * Game.MaxDeskNumber + 1)],
        ]

        for i in (0, 1):
            for n, button in enumerate(self.desk_card_buttons[i]):
                if n % 2 == 0:
                    button.grid(row=2 if i == 0 else 1, column=n, ipadx=0, ipady=hand_card_pad)
                else:
                    button.grid(row=2 if i == 0 else 1, column=n, ipadx=hand_card_pad, ipady=hand_card_pad)

        ######################
        # Right: Deck frame. #
        ######################
        self.deck_number = [tk.IntVar(self, 0), tk.IntVar(self, 0)]

        # Labels of deck numbers.
        self.deck_label_0 = ttk.Label(
            self,
            borderwidth=10,
            textvariable=self.deck_number[0]
        )
        self.deck_label_0.grid(row=0, column=board_frame_width + 1)

        self.deck_label_1 = ttk.Label(
            self,
            borderwidth=10,
            textvariable=self.deck_number[1]
        )
        self.deck_label_1.grid(row=1, column=board_frame_width + 1)

        ############################
        # Some initial operations. #
        ############################

        self.refresh_window()

    def refresh_window(self):
        """Refresh all elements of the game window."""

        self.refresh_minions()
        self.refresh_deck()

    def refresh_minions(self):
        # for element in self.board_frame.winfo_children():
        #     element.destroy()

        for i in (0, 1):
            player = self.game.players[i]

            hand_number = player.hand_number
            desk_number = player.desk_number

            # # Refresh desk.
            # for n, card in enumerate(player.desk):
            #     minion_button = ttk.Button(self.board_frame, text=show_minion(card))
            #     minion_button.grid(row=2 if i == 0 else 1, column=n, padx=10, pady=5)
            for n, button in enumerate(self.desk_card_buttons[i]):
                if n % 2 == 0:
                    button.config(text='\n\n\n\n\n')
                    continue
                idx = n / 2
                if idx >= desk_number:
                    button.config(text='\n\n\n\n\n')
                else:
                    button.config(text=show_minion(player.desk[idx]))

            # Refresh hand.
            for n, button in enumerate(self.hand_card_buttons[i]):
                if n >= hand_number:
                    button.config(text='\n\n\n\n\n')
                else:
                    button.config(text=show_card(player.hand[n]))

    def refresh_deck(self):
        for i in (0, 1):
            self.deck_number[i].set(self.game.players[i].deck_number)

    def _add_selection(self, selection):
        self.selections.append(selection)

    def _clear_selection(self):
        self.selections.clear()

    # Some user operations.
    def game_begin(self):
        self.game.restart_game()
        self.game.dispatch_event_quick(GameBegin)
        self.refresh_window()

    def turn_end(self):
        self.game.dispatch_event_quick(TurnEnd)
        self.refresh_window()

    def test_binding(self, event: tk.Event):
        print('Click', event)
        for name in dir(event):
            if name.startswith('_'):
                continue
            value = getattr(event, name)
            print(name, '=', value, '({})'.format(type(value).__name__))


__all__ = [
    'GameWindow',
]
