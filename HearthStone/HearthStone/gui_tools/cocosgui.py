#! /usr/bin/python
# -*- coding: utf-8 -*-

import pyglet
import cocos
from cocos import layer, text, director, scene, menu

from HearthStone.core import Game

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
            menu.MenuItem('Exit', self.on_quit)
        ]

        self.create_menu(
            items,
            selected_effect=menu.zoom_in(),
            unselected_effect=menu.zoom_out(),
        )

    def on_new_game(self):
        print('New game!')

        # todo start a new game.

    @staticmethod
    def on_quit():
        pyglet.app.exit()


def run_game(game_filename):
    director.director.init(
        caption='HearthStone',
        resizable=True,
        width=640,
        height=480,
    )

    game = Game(game_filename)

    main_scene = scene.Scene()
    main_scene.add(layer.MultiplexLayer(
        MainMenu(game),
    ), z=1)
    main_scene.add(BackgroundLayer(), z=0)

    director.director.run(main_scene)


if __name__ == '__main__':
    run_game('../../test/data/test_basic_mage.json')


__all__ = [
    'BackgroundLayer',
    'run_game',
]
