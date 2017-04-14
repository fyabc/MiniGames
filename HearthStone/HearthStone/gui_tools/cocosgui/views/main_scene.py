#! /usr/bin/python
# -*- coding: utf-8 -*-

"""Game views."""

import pyglet
import cocos
from cocos import layer, text, director, scene, menu, actions

from ..colors import Colors

__author__ = 'fyabc'


class BackgroundLayer(layer.Layer):
    def __init__(self):
        super(BackgroundLayer, self).__init__()

        # Add more other things here


# todo: OptionsMenu


class MainMenu(menu.Menu):
    def __init__(self, controller):
        super().__init__('HearthStone')

        self.ctrl = controller

        # you can override the font that will be used for the title and the items
        # you can also override the font size and the colors. see menu.py for
        # more info
        self.font_title['font_name'] = 'Arial'
        self.font_title['font_size'] = 72
        self.font_title['color'] = Colors['whitesmoke']

        self.font_item['font_name'] = 'Arial'
        self.font_item['color'] = Colors['white']
        self.font_item['font_size'] = 32
        self.font_item_selected['font_name'] = 'Arial'
        self.font_item_selected['color'] = Colors['green1']
        self.font_item_selected['font_size'] = 32

        # [NOTE] Menu can only contain items, it cannot contain other child, such as Label.
        # Menu items
        items = [
            menu.MenuItem('New Game', self.on_new_game),
            menu.MenuItem('Deck', self.on_deck),
            menu.MenuItem('Options', self.on_options),
            menu.MenuItem('Exit', self.on_quit),
        ]

        self.create_menu(
            items,
            selected_effect=menu.shake(),
            unselected_effect=menu.shake_back(),
            # activated_effect=actions.ScaleTo(1.15, duration=0.2),
        )

    def on_new_game(self):
        print('New game!')

        # todo start a new game.

    def on_deck(self):
        print('Decks!')

    def on_options(self):
        print('Options!')

    @staticmethod
    def on_quit():
        pyglet.app.exit()


def get_main_scene(controller):
    main_scene = scene.Scene()

    main_scene.add(layer.MultiplexLayer(
        MainMenu(controller),
    ), z=1)
    main_scene.add(BackgroundLayer(), z=0)

    return main_scene
