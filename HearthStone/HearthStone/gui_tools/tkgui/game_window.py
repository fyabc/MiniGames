#! /usr/bin/python
# -*- coding: utf-8 -*-

import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox

from .selection_manager import SelectionStateMachine
from .tk_ext import ToolTip
from ...cli_tool import show_card, show_minion
from ...game_events.attack import Attack
from ...game_events.basic import GameBegin, TurnEnd
from ...game_events.play import SummonMinion, PlaySpell
from ...utils.basic import WINDOWS

__author__ = 'fyabc'


class GameWindow(ttk.Frame):
    """The Tk game window.

    """

    # [NOTE] Some rules of the variable's name in the layout:
    # There are two players in the game. I am Player 0, opponent is Player 1.

    # Some constants.
    ShowCardWidth = 11

    def __init__(self, game, master=None):
        super(GameWindow, self).__init__(master=master, borderwidth=30)
        self.pack(fill=tk.BOTH)

        self.game = game

        self.game_running = tk.BooleanVar(self, False, 'game_running')
        self.game_running.trace('w', self._on_game_running_changed)

        # todo: add a state machine to manage the selection state.
        # The selection state should be a variable to be traced.
        # For example, when select a minion in hand, then only locations in my desk can be select.
        self.ssm = SelectionStateMachine(self)

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

        self.hand_frames[0].grid(row=2, column=1)
        self.hand_frames[1].grid(row=0, column=1)

        # Desk frame.
        self.desk_frame = ttk.Frame(self, borderwidth=frame_bw)
        self.desk_frame.grid(row=1, column=1, columnspan=1, stick=tk.W + tk.E)

        # Fill the board with Buttons.
        # Buttons between minions should have smaller width.
        card_pad = 1
        card_width = 10

        self.hand_card_buttons = [
            [ttk.Button(
                self.hand_frames[0],
                width=card_width,
                state=tk.DISABLED,
                command=lambda i=i: self.ssm.transform((0, 'hand', i)),
            ) for i in range(self.game.MaxHandNumber)],
            [ttk.Button(
                self.hand_frames[1],
                width=card_width,
                state=tk.DISABLED,
                command=lambda i=i: self.ssm.transform((1, 'hand', i)),
            ) for i in range(self.game.MaxHandNumber)],
        ]

        for i in (0, 1):
            for n, button in enumerate(self.hand_card_buttons[i]):
                button.grid(row=0, column=n, ipadx=card_pad, ipady=card_pad)

        self.desk_card_buttons = [
            [ttk.Button(
                self.desk_frame,
                state=tk.DISABLED,
                command=lambda i=i: self.ssm.transform((0, 'desk', i)),
            ) for i in range(2 * self.game.MaxDeskNumber + 1)],
            [ttk.Button(
                self.desk_frame,
                state=tk.DISABLED,
                command=lambda i=i: self.ssm.transform((1, 'desk', i)),
            ) for i in range(2 * self.game.MaxDeskNumber + 1)],
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
        self.info_frames[0].grid(row=2, column=2, columnspan=1, sticky=tk.N + tk.S)
        self.info_frames[1].grid(row=0, column=2, columnspan=1, sticky=tk.N + tk.S)

        self.deck_number = [tk.IntVar(self, 0), tk.IntVar(self, 0)]
        self.hero_health = [tk.StringVar(self, '0'), tk.StringVar(self, '0')]
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

        # Turn end button.
        self.player_button_frame = ttk.Frame(self, borderwidth=frame_bw)
        self.player_button_frame.grid(row=1, column=2)

        self.player_buttons = [
            [
                ttk.Button(self.player_button_frame,
                           text='Turn End',
                           state=tk.DISABLED,
                           command=self.turn_end,
                           ),
                ttk.Button(self.player_button_frame,
                           text='Skill',
                           state=tk.DISABLED,
                           ),
                ttk.Button(self.player_button_frame,
                           text='Hero',
                           state=tk.DISABLED,
                           command=lambda i=i: self.ssm.transform((i, 'hero', 0))
                           ),
            ] for i in (0, 1)
        ]

        _n_button = len(self.player_buttons[0])
        for i in (0, 1):
            for n, button in enumerate(self.player_buttons[i]):
                if i == 0:
                    _row = n + _n_button
                else:
                    _row = _n_button - 1 - n
                button.grid(row=_row, column=0, pady=3)
                
        # All tooltips.
        self.all_tooltips = {}

        ############################
        # Some initial operations. #
        ############################

        self._set_style()

        self.refresh_window()

    @staticmethod
    def _set_style():
        s = ttk.Style()

        # Tkinter show different on Windows and Ubuntu.
        if WINDOWS:
            s.configure(
                'TButton',
                foreground='black',
                background='black',
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
                    ('disabled', 'purple'),
                    ('pressed', '!focus', 'cyan'),
                    ('active', 'lightblue')
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
        else:
            s.configure(
                'TButton',
                foreground='black',
                background='white',
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
                    ('disabled', 'purple'),
                    ('pressed', '!focus', 'cyan'),
                    ('active', 'lightblue')
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
                background='white',
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
                    button.unbind('<Enter>')
                    button.unbind('<Leave>')

                    idx = n // 2
                    if idx >= desk_number:
                        button.config(text=(' ' * self.ShowCardWidth + '\n') * 5)
                    else:
                        button.config(text=show_minion(player.desk[idx], self.ShowCardWidth))
                        self.all_tooltips[button] = ToolTip(button, player.desk[idx].data['description'])

            # Refresh hand.
            for n, button in enumerate(self.hand_card_buttons[i]):
                if button in self.all_tooltips:
                    self.all_tooltips[button].close()
                
                button.unbind('<Enter>')
                button.unbind('<Leave>')

                if n >= hand_number:
                    button.config(text=(' ' * self.ShowCardWidth + '\n') * 5)
                else:
                    button.config(text=show_card(player.hand[n], self.ShowCardWidth))
                    self.all_tooltips[button] = ToolTip(button, player.hand[n].data['description'])

    def refresh_info(self):
        for i in (0, 1):
            player = self.game.players[i]
            self.deck_number[i].set(player.deck_number)
            self.hero_health[i].set('{}{}'.format(
                player.health,
                '(+{})'.format(player.armor) if player.armor > 0 else '',
            ))
            self.crystal[i].set('{}/{}{}{}'.format(
                player.remain_crystal,
                player.total_crystal,
                '\n({} locked)'.format(player.locked_crystal) if player.locked_crystal > 0 else '',
                '\n({} to be locked)'.format(player.next_locked_crystal) if player.next_locked_crystal > 0 else '',
            ))

    def find_button(self, selection):
        """Find the button from the selection."""

        player_id, location, index = selection

        if location == 'hand':
            return self.hand_card_buttons[player_id][index]
        elif location == 'desk':
            return self.desk_card_buttons[player_id][index]
        elif location == 'hero':
            return self.player_buttons[player_id][2]
        else:
            raise ValueError('Unknown location {}'.format(location))

    def _find_card(self, selection):
        player_id, location, index = selection

        player = self.game.players[player_id]
        if location == 'hand':
            return player.hand[index]
        elif location == 'desk':
            return player.desk[index // 2]
        else:
            raise ValueError('Unknown location {}'.format(location))

    def _on_game_running_changed(self, *args):
        """The callback function when the running status changed.

        Connected to variable `self.game_running`.
        """

        if self.game_running.get():
            self.menu_bar.entryconfig(3, state=tk.NORMAL)
            self.ssm.state.set(0)
        else:
            self.menu_bar.entryconfig(3, state=tk.DISABLED)
            for player_buttons in self.hand_card_buttons:
                for button in player_buttons:
                    button.config(state=tk.DISABLED)
            for player_buttons in self.desk_card_buttons:
                for button in player_buttons:
                    button.config(state=tk.DISABLED)

    # Some user operations.
    def _checked_dispatch(self, event_type, *args, **kwargs):
        end_event = self.game.dispatch_event_quick(event_type, *args, **kwargs)

        if end_event is not None:
            self.refresh_window()

            ok = messagebox.askokcancel(
                'Game End!',
                '''\
The game is end!
Current player: P{}
Loser: P{}
Restart or Quit?
'''.format(end_event.current_player_id, end_event.loser_id)
            )

            if ok:
                self.game_begin()
            else:
                self.quit()

    def game_begin(self):
        self.game_running.set(True)
        self.game.restart_game()
        self._checked_dispatch(GameBegin)
        self.ssm.clear_selection()
        self.ssm.state.set(0)
        self.refresh_window()

    def turn_end(self):
        self._checked_dispatch(TurnEnd)
        self.ssm.clear_selection()
        self.ssm.state.set(0)
        self.refresh_window()

    def try_summon_minion(self, minion, index, target=None):
        self._checked_dispatch(SummonMinion, minion, index, target)
        self.refresh_window()

    def try_attack(self, source, target):
        self._checked_dispatch(Attack, source, target)
        self.refresh_window()

    def try_play_spell(self, spell, target=None):
        self._checked_dispatch(PlaySpell, spell, target)
        self.refresh_window()


__all__ = [
    'GameWindow',
]
