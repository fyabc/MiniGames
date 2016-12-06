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

    # Some constants.
    ShowCardWidth = 7

    def __init__(self, game, master=None):
        super(GameWindow, self).__init__(master=master, borderwidth=30)
        self.pack(fill=tk.BOTH)

        self.game = game

        self.game_running = tk.BooleanVar(self, False, 'game_running')
        self.game_running.trace('w', self._on_game_running_changed)

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
        self.menu_bar.add_command(label='Turn End', command=self.turn_end, state=tk.DISABLED)
        self.menu_bar.add_command(label='Refresh', command=self.refresh_window)
        self.menu_bar.add_cascade(label='Help', menu=self.cascade_menus['Help'])
        self.menu_bar.add_command(label='Quit', command=self.quit)

        ###############################
        # Window Layout.              #
        #                             #
        #  =========================  #
        #  |  |                 |$$|  #
        #  |  |=================|--|  #
        #  |  |  .  .  .  .  .  |26|  #
        #  |  |-----------------|==|  #
        #  |  |  .  .  .  .  .  |26|  #
        #  |  |=================|--|  #
        #  |  |                 |$$|  #
        #  =========================  #
        #                             #
        ###############################

        frame_bw = 5

        ########################
        # Left: History frame. #
        ########################
        self.history_frame = ttk.Frame(self, borderwidth=frame_bw)
        self.history_frame.grid(row=0, column=0, columnspan=4)

        #################################################
        # Center: Game hand frames and game desk frame. #
        #################################################

        # Hand frames.
        self.hand_frames = [
            ttk.Frame(self, borderwidth=frame_bw),
            ttk.Frame(self, borderwidth=frame_bw),
        ]

        self.hand_frames[0].grid(row=3, column=1)
        self.hand_frames[1].grid(row=0, column=1)

        # Desk frame.
        self.desk_frame = ttk.Frame(self, borderwidth=frame_bw)
        self.desk_frame.grid(row=1, column=1, columnspan=2, stick=tk.W + tk.E)

        # Fill the board with Buttons.
        # Buttons between minions should have smaller width.
        card_pad = 1
        card_width = 10

        self.hand_card_buttons = [
            [ttk.Button(
                self.hand_frames[0],
                width=card_width,
                state=tk.DISABLED,
                command=lambda i=i: self._process_selection(0, 'hand', i),
            ) for i in range(Game.MaxHandNumber)],
            [ttk.Button(
                self.hand_frames[1],
                width=card_width,
                state=tk.DISABLED,
                command=lambda i=i: self._process_selection(1, 'hand', i),
            ) for i in range(Game.MaxHandNumber)],
        ]

        for i in (0, 1):
            for n, button in enumerate(self.hand_card_buttons[i]):
                button.grid(row=0, column=n, ipadx=card_pad, ipady=card_pad)

        self.desk_card_buttons = [
            [ttk.Button(
                self.desk_frame,
                state=tk.DISABLED,
                command=lambda i=i: self._process_selection(0, 'desk', i),
            ) for i in range(2 * Game.MaxDeskNumber + 1)],
            [ttk.Button(
                self.desk_frame,
                state=tk.DISABLED,
                command=lambda i=i: self._process_selection(1, 'desk', i),
            ) for i in range(2 * Game.MaxDeskNumber + 1)],
        ]

        for i in (0, 1):
            for n, button in enumerate(self.desk_card_buttons[i]):
                button.grid(row=1 if i == 0 else 0, column=n, ipadx=card_pad, ipady=card_pad)
                if n % 2 == 0:
                    button.config(width=0)
                else:
                    button.config(width=card_width)

        ######################
        # Right: Info frame. #
        ######################
        self.info_frames = [
            ttk.LabelFrame(
                self,
                borderwidth=frame_bw,
                labelanchor=tk.N,
                text='Player 0 Information',
            ),
            ttk.LabelFrame(
                self,
                borderwidth=frame_bw,
                labelanchor=tk.N,
                text='Player 1 Information',
            ),
        ]
        self.info_frames[0].grid(row=3, column=2, columnspan=1, sticky=tk.N + tk.S)
        self.info_frames[1].grid(row=0, column=2, columnspan=1, sticky=tk.N + tk.S)

        self.deck_number = [tk.IntVar(self, 0), tk.IntVar(self, 0)]
        self.hero_health = [tk.IntVar(self, 0), tk.IntVar(self, 0)]
        self.crystal = [tk.StringVar(self, '0/0'), tk.StringVar(self, '0/0')]

        # Add information name and value labels.
        for i in (0, 1):
            info_frame = self.info_frames[i]
            health_name_label = ttk.Label(
                info_frame,
                text='Health:',
                foreground='darkblue',
            )
            deck_number_name_label = ttk.Label(
                info_frame,
                text='Deck Number:',
                foreground='darkgreen',
            )
            crystal_name_label = ttk.Label(
                info_frame,
                text='Mana Crystal:',
                foreground='purple',
            )

            health_label = ttk.Label(
                info_frame,
                textvariable=self.hero_health[i],
                foreground='darkblue',
            )

            deck_number_label = ttk.Label(
                info_frame,
                textvariable=self.deck_number[i],
                foreground='darkgreen',
            )

            crystal_label = ttk.Label(
                info_frame,
                textvariable=self.crystal[i],
                foreground='purple',
            )

            health_name_label.grid(row=0, column=0, stick=tk.W)
            deck_number_name_label.grid(row=1, column=0, stick=tk.W)
            crystal_name_label.grid(row=2, column=0, stick=tk.W)
            health_label.grid(row=0, column=1, stick=tk.W)
            deck_number_label.grid(row=1, column=1, stick=tk.W)
            crystal_label.grid(row=2, column=1, stick=tk.W)

        ############################
        # Some initial operations. #
        ############################

        self._set_style()

        self.refresh_window()

    def _set_style(self):
        s = ttk.Style()

        s.configure(
            'TButton',
            background='black',
            foreground='black',
            highlightthickness='20',
            font=('Microsoft YaHei UI', 9),
        )

        s.map(
            'TButton',
            foreground=[
                ('pressed', 'red'),
                ('active', 'green')
            ],
            background=[
                ('pressed', '!focus', 'cyan'),
                ('active', 'blue')
            ],
            highlightcolor=[
                ('focus', 'blue'),
                ('!focus', 'red')
            ],
            relief=[
                ('pressed', 'groove'),
                ('!pressed', 'ridge')
            ],
        )

        s.configure(
            'Selected.TButton',
            foreground='green',
            background='green',
            highlightthickness='20',
            font=('Microsoft YaHei UI', 9),
        )

    def refresh_window(self):
        """Refresh all elements of the game window."""

        self.refresh_minions()
        self.refresh_info()

    def refresh_minions(self):
        # for element in self.board_frame.winfo_children():
        #     element.destroy()

        for i in (0, 1):
            player = self.game.players[i]

            hand_number = player.hand_number
            desk_number = player.desk_number

            # Refresh desk.
            for n, button in enumerate(self.desk_card_buttons[i]):
                if n % 2 == 0:
                    button.config(text='\n' * 5)
                else:
                    idx = n / 2
                    if idx >= desk_number:
                        button.config(text=(' ' * self.ShowCardWidth + '\n') * 5)
                    else:
                        button.config(text=show_minion(player.desk[idx], self.ShowCardWidth))

            # Refresh hand.
            for n, button in enumerate(self.hand_card_buttons[i]):
                if n >= hand_number:
                    button.config(text=(' ' * self.ShowCardWidth + '\n') * 5)
                else:
                    button.config(text=show_card(player.hand[n], self.ShowCardWidth))

    def refresh_info(self):
        for i in (0, 1):
            player = self.game.players[i]
            self.deck_number[i].set(player.deck_number)
            self.hero_health[i].set(player.health)
            self.crystal[i].set('{}/{}{}{}'.format(
                player.remain_crystal,
                player.total_crystal,
                '\n({} locked)'.format(player.locked_crystal) if player.locked_crystal > 0 else '',
                '\n({} to be locked)'.format(player.next_locked_crystal) if player.next_locked_crystal > 0 else '',
            ))

    def _find_button(self, selection):
        player_id, location, index = selection

        if location == 'hand':
            return self.hand_card_buttons[player_id][index]
        elif location == 'desk':
            return self.desk_card_buttons[player_id][index]
        else:
            raise ValueError('Unknown location {}'.format(location))

    def _process_selection(self, player_id, location, index):
        print(player_id, location, index)

        if not self.game_running.get():
            return

        selection = player_id, location, index
        button = self._find_button(selection)

        if selection == self.selections[-1]:
            # If the selection is same as the last selection, make it unselected.
            self.selections.remove(selection)
            button.config(style='TButton')
        else:
            # Else, check if it satisfied the condition of some operations (summon, attack, etc.)
            self.selections.append(selection)
            button.config(style='Selected.TButton')

    def _on_game_running_changed(self, *args):
        """The callback function when the running status changed.

        Connected to variable `self.game_running`.
        """

        if self.game_running.get():
            self.menu_bar.entryconfig(3, state=tk.NORMAL)
            for player_buttons in self.hand_card_buttons:
                for button in player_buttons:
                    button.config(state=tk.NORMAL)
            for player_buttons in self.desk_card_buttons:
                for button in player_buttons:
                    button.config(state=tk.NORMAL)
        else:
            self.menu_bar.entryconfig(3, state=tk.DISABLED)
            for player_buttons in self.hand_card_buttons:
                for button in player_buttons:
                    button.config(state=tk.DISABLED)
            for player_buttons in self.desk_card_buttons:
                for button in player_buttons:
                    button.config(state=tk.DISABLED)

    # Some user operations.
    def game_begin(self):
        self.game_running.set(True)
        self.game.restart_game()
        self.game.dispatch_event_quick(GameBegin)
        self.refresh_window()

    def turn_end(self):
        self.game.dispatch_event_quick(TurnEnd)
        self.refresh_window()

    def _summon_minion(self, index, location):
        pass

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
