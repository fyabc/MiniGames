#! /usr/bin/python
# -*- coding: utf-8 -*-

import pyglet
import cocos
from cocos import layer, text, director, scene, menu, actions

from ...core import Game

__author__ = 'fyabc'


class BackgroundLayer(layer.Layer):
    def __init__(self):
        super(BackgroundLayer, self).__init__()

        # Add more other things here


class MainMenu(menu.Menu):
    def __init__(self, game):
        super().__init__('HearthStone')

        self.game = game

        # [NOTE] Menu can only contains items, it cannot contain other child, such as Label.

        # Menu items
        items = [
            menu.MenuItem('New Game', self.on_new_game),
            menu.MenuItem('Exit', self.on_quit),
            menu.MenuItem('Deck', self.on_deck),
        ]

        self.create_menu(
            items,
            selected_effect=menu.shake(),
            unselected_effect=menu.shake_back(),
            activated_effect=actions.ScaleTo(1.15, duration=0.2),
        )

    def on_new_game(self):
        print('New game!')

        # todo start a new game.

    def on_deck(self):
        print('Decks!')

    @staticmethod
    def on_quit():
        pyglet.app.exit()


def run_game(game_filename):
    director.director.init(
        caption='HearthStone',
        resizable=True,
        width=800,
        height=600,
    )

    game = Game(game_filename)

    main_scene = scene.Scene()
    main_scene.add(layer.MultiplexLayer(
        MainMenu(game),
    ), z=1)
    main_scene.add(BackgroundLayer(), z=0)

    director.director.run(main_scene)


__all__ = [
    'run_game',
]
