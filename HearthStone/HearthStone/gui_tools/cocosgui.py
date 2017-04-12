#! /usr/bin/python
# -*- coding: utf-8 -*-

from cocos import layer, text, director, scene

from HearthStone.core import Game

__author__ = 'fyabc'


class MainGameLayer(layer.Layer):
    def __init__(self, game):
        super(MainGameLayer, self).__init__()

        self.game = game

        self.add(text.Label(
            text='HearthStone Game',
            position=(320, 460),
            font_name='Microsoft YaHei UI',
            font_size=24,
            anchor_x='center',
            anchor_y='center',
        ))


def run_game(game_filename):
    director.director.init(
        caption='HearthStone',
        resizable=True,
    )

    game = Game(game_filename)

    game_layer = MainGameLayer(game)
    main_scene = scene.Scene(game_layer)

    director.director.run(main_scene)


if __name__ == '__main__':
    run_game('../../test/data/test_basic_mage.json')


__all__ = [
    'MainGameLayer',
    'run_game',
]
