#! /usr/bin/python
# -*- coding: utf-8 -*-

from functools import partial

from cocos import director, draw, scene
from cocos.scenes import transitions

from .utils.active import ActiveLayer, ActiveLabel
from .utils.basic import pos, pos_y, notice
from .utils.layers import BackgroundLayer, BasicButtonsLayer
from ..utils.constants import Colors
from ...game.core import Game

__author__ = 'fyabc'


class SelectDeckLayer(ActiveLayer):
    RightL = 0.7
    RightCX = (1 + RightL) / 2
    LeftCX = RightL / 2
    P1CX, P2CX = RightL / 4, RightL * 3 / 4
    PlayersCX = (RightL / 4, RightL * 3 / 4)

    DeckListT = 0.9
    DeckListB = 0.25
    DeckShowS = 10

    def __init__(self, ctrl):
        super().__init__(ctrl)

        self.add(ActiveLabel.hs_style(
            'Start Game', pos(self.RightCX, 0.15),
            callback=self._on_start_game,
            font_size=36, anchor_x='center',
        ), name='button_start_game')

        # All deck buttons, current show start indices and selected decks.
        self.deck_button_lists = [[], []]
        self.deck_show_start = [0, 0]
        self.selected_decks = [None, None]

        # Up and down buttons.
        for player_id in (0, 1):
            for is_down in (False, True):
                self.add(ActiveLabel.hs_style(
                    '[ {} ]'.format('↓' if is_down else '↑'),
                    pos(self.PlayersCX[player_id] + 0.05 * (1 if is_down else -1), 0.15),
                    callback=lambda player_id_=player_id, is_down_=is_down: self._scroll_decks(player_id_, is_down_),
                    font_size=28, anchor_x='center', anchor_y='center', bold=True,
                ), name='button_p{}_decks_{}'.format(player_id, 'down' if is_down else 'up'))

    def on_enter(self):
        super().on_enter()

        def _select_deck(label, player_id_, deck_):
            # Undo render of all deck buttons, then render this (selected) label
            for deck_button in self.deck_button_lists[player_id_]:
                assert isinstance(deck_button, ActiveLabel)
                if getattr(deck_button, '_deck_selected', None) is True:
                    delattr(deck_button, '_deck_selected')
                    deck_button.element.text = deck_button.element.text[2:-2]
            label.element.text = '[ {} ]'.format(label.element.text)
            setattr(label, '_deck_selected', True)
            self.selected_decks[player_id_] = deck_

        # Load decks and reset deck selections.
        self.deck_show_start = [0, 0]
        self.selected_decks = [None, None]
        self.deck_button_lists = [[
            ActiveLabel.hs_style(
                deck.name, pos(self.PlayersCX[player_id], 1.0),
                callback=partial(_select_deck, player_id_=player_id, deck_=deck),
                anchor_x='center', anchor_y='center', self_in_callback=True,)
            for i, deck in enumerate(self.ctrl.user.decks)
        ] for player_id in (0, 1)]
        self._refresh_deck_buttons()

        # Default: select first decks if exists (by call callback directly).
        for player_id in (0, 1):
            if self.deck_button_lists[player_id]:
                self.deck_button_lists[player_id][0].call()

    def on_exit(self):
        # Clear deck buttons.
        self._remove_decks_buttons()
        self.deck_button_lists = [[], []]
        self.deck_show_start = [0, 0]
        self.selected_decks = [None, None]

        return super().on_exit()

    def _refresh_deck_buttons(self):
        """Refresh deck buttons with given show start."""
        self._remove_decks_buttons()
        for player_id, deck_button_list in enumerate(self.deck_button_lists):
            for i, deck_button in enumerate(deck_button_list):
                deck_button.y = pos_y(self.DeckListT - (self.DeckListT - self.DeckListB) *
                                      (i - self.deck_show_start[player_id]) / (self.DeckShowS - 1))
                if self.deck_show_start[player_id] <= i < self.deck_show_start[player_id] + self.DeckShowS:
                    self.add(deck_button)

    def _remove_decks_buttons(self):
        """Remove all deck buttons from this layer."""
        for deck_button_list in self.deck_button_lists:
            for deck_button in deck_button_list:
                if deck_button in self:
                    self.remove(deck_button)

    def _on_start_game(self):
        if any(map(lambda e: e is None, self.selected_decks)):
            notice(self, 'Must select two decks!')
            return
        # Create new game, register callback and start game.
        self.ctrl.game = Game(frontend=self.ctrl)
        self.ctrl.get_node('game/board').prepare_start_game(self.ctrl.game, self.selected_decks)

        director.director.replace(transitions.FadeTransition(self.ctrl.get('game'), duration=0.5))

    def _scroll_decks(self, player_id, is_down):
        if is_down:
            if self.deck_show_start[player_id] + self.DeckShowS >= len(self.deck_button_lists[player_id]):
                return
        else:
            if self.deck_show_start[player_id] == 0:
                return
        self.deck_show_start[player_id] += int(is_down) * 2 - 1
        self._refresh_deck_buttons()


def get_select_deck_bg():
    right_l = SelectDeckLayer.RightL
    left_cx = SelectDeckLayer.LeftCX

    bg = BackgroundLayer()
    bg.add(draw.Line(pos(right_l, .0), pos(right_l, 1.), Colors['white'], 2))
    bg.add(draw.Line(pos(left_cx, .0), pos(left_cx, 1.), Colors['white'], 2))

    return bg


def get_select_deck_scene(controller):
    select_deck_scene = scene.Scene()

    select_deck_scene.add(get_select_deck_bg(), z=0, name='background')
    select_deck_scene.add(BasicButtonsLayer(controller), z=1, name='basic_buttons')
    select_deck_scene.add(SelectDeckLayer(controller), z=2, name='main')

    return select_deck_scene


__all__ = [
    'get_select_deck_scene',
]
