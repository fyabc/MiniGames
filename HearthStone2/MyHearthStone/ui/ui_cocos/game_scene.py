#! /usr/bin/python
# -*- coding: utf-8 -*-

from functools import partial

from cocos import scene, draw, director
from cocos.scenes import transitions

from .utils import pos, pos_y
from ...utils.draw.constants import Colors
from .basic_components import *
from ...game.core import Game

__author__ = 'fyabc'


class SelectDeckLayer(ActiveLayer):
    RightB = 0.7
    RightC = (1 + RightB) / 2
    LeftC = RightB / 2
    P1C, P2C = RightB / 4, RightB * 3 / 4
    PlayersC = (RightB / 4, RightB * 3 / 4)

    DeckListTop = 0.9
    DeckListBottom = 0.25
    DeckShowSize = 10

    def __init__(self, ctrl):
        super().__init__(ctrl)

        self.add(ActiveLabel.hs_style(
            'Start Game', pos(self.RightC, 0.15),
            callback=self.on_start_game,
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
                    pos(self.PlayersC[player_id] + 0.05 * (1 if is_down else -1), 0.15),
                    callback=lambda player_id_=player_id, is_down_=is_down: self.scroll_decks(player_id_, is_down_),
                    font_size=28, anchor_x='center',
                ), name='button_p{}_decks_{}'.format(player_id, 'down' if is_down else 'up'))

    def on_enter(self):
        super().on_enter()

        def select_deck(label, player_id_, deck_):
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
                deck.name, pos(self.PlayersC[player_id], 1.0),
                callback=partial(select_deck, player_id_=player_id, deck_=deck),
                anchor_x='center', anchor_y='center', self_in_callback=True,)
            for i, deck in enumerate(self.ctrl.user.decks)
        ] for player_id in (0, 1)]
        self._refresh_deck_buttons()

        # Default: select first decks if exists (by call callback directly).
        for player_id in (0, 1):
            if self.deck_button_lists[player_id]:
                self.deck_button_lists[player_id][0].callback(self.deck_button_lists[player_id][0])

    def on_exit(self):
        super().on_exit()

        # Clear deck buttons.
        self._remove_decks_buttons()
        self.deck_button_lists = [[], []]
        self.deck_show_start = [0, 0]
        self.selected_decks = [None, None]

    def _refresh_deck_buttons(self):
        """Refresh deck buttons with given show start."""
        self._remove_decks_buttons()
        for player_id, deck_button_list in enumerate(self.deck_button_lists):
            for i, deck_button in enumerate(deck_button_list):
                deck_button.y = pos_y(self.DeckListTop - (self.DeckListTop - self.DeckListBottom) *
                                      (i - self.deck_show_start[player_id]) / (self.DeckShowSize - 1))
                if self.deck_show_start[player_id] <= i < self.deck_show_start[player_id] + self.DeckShowSize:
                    self.add(deck_button)

    def _remove_decks_buttons(self):
        """Remove all deck buttons from this layer."""
        for deck_button_list in self.deck_button_lists:
            for deck_button in deck_button_list:
                if deck_button in self:
                    self.remove(deck_button)

    def on_start_game(self):
        if any(map(lambda e: e is None, self.selected_decks)):
            notice(self, 'Must select two decks!',
                   position=pos(0.5, 0.5), anchor_y='center', font_size=32, color=Colors['yellow1'], time=1.5)
            return

        self.ctrl.game = Game(frontend=self.ctrl)
        start_game_iter = self.ctrl.game.start_game(self.selected_decks, mode='standard')

        game_board_layer = self.ctrl.get_node('game/board')
        game_board_layer.start_game_iter = start_game_iter
        director.director.replace(transitions.FadeTransition(self.ctrl.get('game'), duration=1.0))

    def scroll_decks(self, player_id, is_down):
        if is_down:
            if self.deck_show_start[player_id] + self.DeckShowSize >= len(self.deck_button_lists[player_id]):
                return
        else:
            if self.deck_show_start[player_id] == 0:
                return

        self.deck_show_start[player_id] += int(is_down) * 2 - 1

        self._refresh_deck_buttons()


def get_select_deck_bg():
    right_b = SelectDeckLayer.RightB
    left_c = SelectDeckLayer.LeftC

    bg = BackgroundLayer()
    bg.add(draw.Line(pos(right_b, .0), pos(right_b, 1.), Colors['white'], 2))
    bg.add(draw.Line(pos(left_c, .0), pos(left_c, 1.), Colors['white'], 2))

    return bg


def get_select_deck_scene(controller):
    select_deck_scene = scene.Scene()

    select_deck_scene.add(get_select_deck_bg(), z=0, name='background')
    select_deck_scene.add(BasicButtonsLayer(controller), z=1, name='basic_buttons')
    select_deck_scene.add(SelectDeckLayer(controller), z=2, name='main')

    return select_deck_scene


class GameBoardLayer(ActiveLayer):
    RightB = 0.88  # Border of right pane
    RightC = (1 + RightB) / 2  # Center of right pane
    HeroB = 0.66  # Border of hero pane
    TurnEndBtnWidth = 0.1  # Width of turn end button
    TurnEndBtnTop, TurnEndBtnBottom = 0.5 + TurnEndBtnWidth / 2, 0.5 - TurnEndBtnWidth / 2
    HandRatio = 0.23  # Size ratio of hand cards

    def __init__(self, ctrl):
        super().__init__(ctrl)

        ctrl.game.add_resolve_callback(self.update_content)

        # Start game iterator returned from `Game.start_game`. Sent from select deck layer.
        self.start_game_iter = None

        # Card sprites
        self.hand_sprites = [[] for _ in range(2)]
        self.deck_sprites = [[] for _ in range(2)]

    def update_content(self, event_or_trigger, current_event):
        """Update the game board content, called by game event engine."""

        pass


class GameButtonsLayer(ActiveLayer):
    def __init__(self, ctrl):
        super().__init__(ctrl)

        self.turn_end = ActiveLabel.hs_style(
            'End Turn', pos(GameBoardLayer.RightC, 0.5),
            callback=self.on_turn_end,
            font_size=24, anchor_x='center', anchor_y='center',)
        self.add(self.turn_end, name='button_turn_end')

    def on_turn_end(self):
        pass


def get_game_bg():
    right_b = GameBoardLayer.RightB
    hero_b = GameBoardLayer.HeroB
    te_btn_top, te_btn_bottom = GameBoardLayer.TurnEndBtnTop, GameBoardLayer.TurnEndBtnBottom
    hand_ratio = GameBoardLayer.HandRatio

    bg = BackgroundLayer()

    # Lines.
    bg.add(draw.Line(pos(right_b, .0), pos(right_b, 1.), Colors['white'], 2))
    bg.add(draw.Line(pos(.0, .5), pos(right_b, .5), Colors['white'], 2))
    bg.add(draw.Line(pos(right_b, te_btn_top), pos(1.0, te_btn_top), Colors['white'], 2))
    bg.add(draw.Line(pos(right_b, te_btn_bottom), pos(1.0, te_btn_bottom), Colors['white'], 2))
    bg.add(draw.Line(pos(.0, hand_ratio), pos(hero_b, hand_ratio), Colors['white'], 2))
    bg.add(draw.Line(pos(.0, 1 - hand_ratio), pos(hero_b, 1 - hand_ratio), Colors['white'], 2))
    bg.add(draw.Line(pos(hero_b, .0), pos(hero_b, 1.), Colors['white'], 2))

    return bg


def get_game_scene(controller):
    game_scene = scene.Scene()

    game_scene.add(get_game_bg(), z=0, name='background')
    game_scene.add(GameButtonsLayer(controller), z=1, name='buttons')
    game_scene.add(GameBoardLayer(controller), z=2, name='board')

    return game_scene


__all__ = [
    'get_select_deck_scene',
    'get_game_scene',
]
