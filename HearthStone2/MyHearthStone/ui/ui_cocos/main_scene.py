#! /usr/bin/python
# -*- coding: utf-8 -*-

"""The main scene of the cocos-single frontend.

This is one of the views in MVC pattern.
"""

import pyglet
from cocos import director, layer, scene, menu
from cocos.scenes import transitions

from .utils.basic import set_menu_style
from .utils.layers import BackgroundLayer, BasicButtonsLayer

__author__ = 'fyabc'


class MainMenu(menu.Menu):
    """Main menu. Index of parent: 0"""

    def __init__(self, controller):
        super().__init__('HearthStone')
        self.ctrl = controller

        set_menu_style(self)

        # [NOTE] Menu can only contain items, it cannot contain other child, such as Label.
        # Menu items
        items = [
            menu.MenuItem('New Game', self.on_new_game),
            menu.MenuItem('Deck', self.on_collections),
            menu.MenuItem('Options', self.on_options),
            menu.MenuItem('Exit', self.on_quit),
        ]

        self.create_menu(items)

    def on_new_game(self):
        director.director.replace(transitions.FadeTransition(self.ctrl.scenes['select_deck'], duration=1.0))

    def on_collections(self):
        director.director.replace(transitions.FadeTransition(self.ctrl.scenes['collection'], duration=1.0))

    def on_options(self):
        self.parent.switch_to(1)

    def on_quit(self):
        """On key ESCAPE."""

        pyglet.app.exit()


class OptionsMenu(menu.Menu):
    """Options menu. Index in parent: 1"""

    def __init__(self, controller):
        super().__init__('Options')
        self.ctrl = controller

        set_menu_style(self)

        items = [
            menu.ToggleMenuItem('Show FPS:', self.on_show_fps, director.director.show_FPS),
            menu.MenuItem('FullScreen', self.on_full_screen),
            menu.MenuItem('Back', self.on_quit)
        ]

        self.create_menu(items)

    @staticmethod
    def on_show_fps(value):
        director.director.show_FPS = bool(value)

    @staticmethod
    def on_full_screen():
        director.director.window.set_fullscreen(not director.director.window.fullscreen)

    def on_quit(self):
        self.parent.switch_to(0)


def get_main_scene(controller):
    main_scene = scene.Scene()

    main_scene.add(BackgroundLayer(), z=0, name='background')
    main_scene.add(BasicButtonsLayer(controller, back=False), z=1, name='basic_buttons')
    main_scene.add(layer.MultiplexLayer(
        MainMenu(controller),
        OptionsMenu(controller),
    ), z=2, name='main')

    return main_scene


__all__ = [
    'get_main_scene',
]
