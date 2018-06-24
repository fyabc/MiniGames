#! /usr/bin/python
# -*- coding: utf-8 -*-

from functools import partial

from cocos import director, draw, scene, layer
from cocos.scenes import transitions

from .utils.active import *
from .utils.basic import pos, notice
from .utils.layers import BackgroundLayer, BasicButtonsLayer
from ..utils.constants import Colors
from ...utils.game import Klass
from ...game.core import Game
from ...game.default_data import PracticeDecks, get_inn_keeper

__author__ = 'fyabc'


class AdventureSelectLayer(ActiveLayer):
    SelectR = 0.22
    SelectCX = SelectR / 2
    SelectArrowY = 0.15
    SelectListT, SelectListB = 0.95, 0.25
    SelectSize = 10

    def __init__(self, ctrl, main_layer):
        super().__init__(ctrl)
        self.main_layer = main_layer

        self._select_dict, self._select_refresh = active_scroll_list(self, {
            'CX': self.SelectCX,
            'ListT': self.SelectListT,
            'ListB': self.SelectListB,
            'ArrowY': self.SelectArrowY,
            'Size': self.SelectSize,
        })
    
    def on_enter(self):
        super().on_enter()

        self._build_buttons_from_main_layer()
        scroll_list_enter(self._select_dict, self._select_refresh)

    def on_exit(self):
        scroll_list_exit(self, self._select_dict)

        return super().on_exit()

    def _build_buttons_from_main_layer(self):
        fn = active_labels_group_select_fn(self._select_dict['buttons'], prefix='mode')

        def _mode_selected(clicked_button, i):
            fn(clicked_button)
            self.main_layer.switch_to(i)

        self._select_dict['buttons'] = [
            ActiveLabel.hs_style(
                layer_.name, pos(0.0, 1.0),
                callback=partial(_mode_selected, i=i),
                anchor_x='center', anchor_y='center', self_in_callback=True,
            )
            for i, layer_ in enumerate(self.main_layer.layers)
        ]


class PracticeModeLayer(ActiveLayer):
    BorderL = AdventureSelectLayer.SelectR

    DeckR = BorderL + 0.35
    DeckCX = (BorderL + DeckR) / 2
    DeckArrowY = 0.15
    DeckListT, DeckListB = 0.9, 0.25
    DeckListSize = 10

    DiffX1, DiffX2 = DeckR + (1.0 - DeckR) * 0.25, DeckR + (1.0 - DeckR) * 0.75
    DiffB = 0.8
    DiffY = (1.0 + DiffB) / 2

    KlassL, KlassR = DeckR + (1.0 - DeckR) * 0.2, DeckR + (1.0 * DeckR) * 0.8
    KlassXS = 3
    KlassT, KlassB = 0.7, 0.25

    StartX = (1.0 + DeckR) / 2
    StartY = DeckArrowY

    def __init__(self, ctrl):
        super().__init__(ctrl)
        self.name = 'Practice Mode'

        self.add(draw.Line(pos(self.DeckR, 0.0), pos(self.DeckR, 1.0), Colors['white'], 2))

        self._deck_dict, self._deck_refresh = active_scroll_list(self, {
            'CX': self.DeckCX,
            'ListT': self.DeckListT,
            'ListB': self.DeckListB,
            'ArrowY': self.DeckArrowY,
            'Size': self.DeckListSize,
        })

        self.difficulty_group = []
        self.difficulty = None     # False = Normal, True = Expert
        self._build_difficulty_buttons()

        self.ai_class_group = []
        self.ai_class = None
        self._build_ai_class_buttons()

        self.add(ActiveLabel.hs_style(
            'Start Game', pos(self.StartX, self.StartY),
            callback=self._on_start_game,
            font_size=36, anchor_x='center',
        ))

    def on_enter(self):
        super().on_enter()

        self._build_deck_buttons()

        scroll_list_enter(self._deck_dict, self._deck_refresh)

    def on_exit(self):
        scroll_list_exit(self, self._deck_dict)

        return super().on_exit()

    def _build_deck_buttons(self):
        fn = active_labels_group_select_fn(self._deck_dict['buttons'], prefix='deck')

        def _deck_selected(clicked_button, deck):
            fn(clicked_button)
            self._deck_dict['selected'] = deck

        self._deck_dict['buttons'].extend([
            ActiveLabel.hs_style(
                deck.name, pos(0.0, 1.0),
                callback=partial(_deck_selected, deck=deck),
                anchor_x='center', anchor_y='center', self_in_callback=True,
            )
            for deck in self.ctrl.user.decks
        ])

    def _build_difficulty_buttons(self):
        fn = active_labels_group_select_fn(self.difficulty_group, 'difficulty')

        def _diff_selected(clicked_button, diff):
            fn(clicked_button)
            self.difficulty = diff

        self.difficulty_group.extend([
            ActiveLabel.hs_style(
                'Normal', pos(self.DiffX1, self.DiffY),
                callback=partial(_diff_selected, diff=False),
                anchor_x='center', anchor_y='center', self_in_callback=True,
            ),
            ActiveLabel.hs_style(
                'Expert', pos(self.DiffX2, self.DiffY),
                callback=partial(_diff_selected, diff=True),
                anchor_x='center', anchor_y='center', self_in_callback=True,
            ),
        ])

        for button in self.difficulty_group:
            self.try_add(button)

    def _build_ai_class_buttons(self):
        fn = active_labels_group_select_fn(self.ai_class_group, 'ai_class')

        def _ai_class_selected(clicked_button, klass_):
            fn(clicked_button)
            self.ai_class = klass_

        MaxY = (len(Klass.Idx2Str) - 1) // self.KlassXS + 1
        for klass, name in Klass.Idx2Str.items():
            if klass == Klass.Neutral:
                continue
            y, x = divmod(klass - 1, self.KlassXS)
            self.ai_class_group.append(ActiveLabel.hs_style(
                name, pos(self.KlassL + x * (self.KlassR - self.KlassL) / self.KlassXS,
                          self.KlassT - y * (self.KlassT - self.KlassB) / MaxY),
                callback=partial(_ai_class_selected, klass_=klass),
                anchor_x='center', anchor_y='center', self_in_callback=True,
            ))

        for button in self.ai_class_group:
            self.try_add(button)

    def _on_start_game(self):
        if self._deck_dict['selected'] is None:
            notice(self, 'Must select a deck!')
            return
        if self.difficulty is None:
            notice(self, 'Must select a difficulty!')
            return
        if self.ai_class is None:
            notice(self, 'Must select a class as opponent!')
            return

        self.ctrl.game = Game()

        inn_keeper = get_inn_keeper()
        inn_keeper.create_agent(self.ctrl.game, player_id=1)

        self.ctrl.get_node('game/board').prepare_start_game(
            self.ctrl.game, [
                self._deck_dict['selected'],
                PracticeDecks['Expert' if self.difficulty else 'Normal'][self.ai_class]],
            users=[self.ctrl.user, inn_keeper],
            main_player_id=0,
            where_come_from=self.ctrl.get('adventure')
        )

        director.director.replace(transitions.FadeTransition(self.ctrl.get('game'), duration=0.5))


def get_adventure_bg():
    select_r = AdventureSelectLayer.SelectR

    bg = BackgroundLayer()
    bg.add(draw.Line(pos(select_r, .0), pos(select_r, 1.), Colors['white'], 2))

    return bg


def get_adventure_scene(controller):
    adventure_scene = scene.Scene()

    adventure_scene.add(get_adventure_bg(), z=0, name='background')
    adventure_scene.add(BasicButtonsLayer(controller), z=1, name='basic_buttons')

    main_layer = layer.MultiplexLayer(
        PracticeModeLayer(controller),
    )

    adventure_scene.add(main_layer, z=2, name='main')
    adventure_scene.add(AdventureSelectLayer(controller, main_layer), z=3, name='select')

    return adventure_scene
