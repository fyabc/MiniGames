#! /usr/bin/python
# -*- coding: utf-8 -*-

from cocos import scene, draw, director
from cocos.scenes import transitions

from .utils import pos
from ...utils.draw.constants import Colors
from .basic_components import *

__author__ = 'fyabc'


class SelectDeckLayer(ActiveLayer):
    RightB = 0.7
    RightC = (1 + RightB) / 2

    def __init__(self, ctrl):
        super().__init__(ctrl)

        self.start_game = ActiveLabel.hs_style(
            'Start Game',
            pos(self.RightC, 0.15),
            callback=self.on_start_game,
            font_size=36,
            anchor_x='center',
        )
        self.add(self.start_game, name='button_start_game')

    def on_start_game(self):
        director.director.replace(transitions.FadeTransition(self.ctrl.get('game'), duration=1.0))


def get_select_deck_bg():
    right_b = SelectDeckLayer.RightB

    bg = BackgroundLayer()
    bg.add(draw.Line(pos(right_b, .0), pos(right_b, 1.), Colors['white'], 2))

    return bg


def get_select_deck_scene(controller):
    select_deck_scene = scene.Scene()

    select_deck_scene.add(get_select_deck_bg(), z=0, name='background')
    select_deck_scene.add(BasicButtonsLayer(controller), z=1, name='basic_buttons')
    select_deck_scene.add(SelectDeckLayer(controller), z=2, name='main')

    return select_deck_scene


class GameBoardLayer(ActiveLayer):
    RightB = 0.88               # Border of right pane
    RightC = (1 + RightB) / 2   # Center of right pane
    HeroB = 0.66                # Border of hero pane
    TurnEndBtnWidth = 0.1       # Width of turn end button
    TurnEndBtnTop, TurnEndBtnBottom = 0.5 + TurnEndBtnWidth / 2, 0.5 - TurnEndBtnWidth / 2
    HandRatio = 0.23            # Size ratio of hand cards

    def __init__(self, ctrl):
        super().__init__(ctrl)

        ctrl.game.add_resolve_callback(self.update_content)

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
            'End Turn',
            pos(GameBoardLayer.RightC, 0.5),
            callback=self.on_turn_end,
            font_size=24,
            anchor_x='center',
            anchor_y='center',
        )
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
