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
from ...utils.constants import C

__author__ = 'fyabc'


class MainLayer(layer.MultiplexLayer):
    MainID, OptionsID = 0, 1

    def get_options_menu(self):
        return self.layers[self.OptionsID]


class MainMenu(menu.Menu):
    """Main menu."""

    def __init__(self, controller):
        super().__init__('HearthStone')
        self.ctrl = controller

        set_menu_style(self)

        # [NOTE] Menu can only contain items, it cannot contain other child, such as Label.
        # Menu items
        items = [
            menu.MenuItem('New Game', self.on_new_game),
            menu.MenuItem('New Adventure', self.on_new_adventure),
            menu.MenuItem('Deck', self.on_collections),
            menu.MenuItem('Options', self.on_options),
            menu.MenuItem('Exit', self.on_quit),
        ]

        self.create_menu(items)

    def on_new_game(self):
        director.director.replace(transitions.FadeTransition(self.ctrl.scenes['select_deck'], duration=1.0))

    def on_new_adventure(self):
        director.director.replace(transitions.FadeTransition(self.ctrl.scenes['adventure'], duration=1.0))

    def on_collections(self):
        director.director.replace(transitions.FadeTransition(self.ctrl.scenes['collection'], duration=1.0))

    def on_options(self):
        self.parent.switch_to(MainLayer.OptionsID)

    def on_quit(self):
        """On key ESCAPE."""

        pyglet.app.exit()


class OptionsMenu(menu.Menu):
    """Options menu."""

    def __init__(self, controller):
        super().__init__('Options')
        self.ctrl = controller

        set_menu_style(self)

        items = [
            menu.ToggleMenuItem('Show FPS:', self.on_show_fps, director.director.show_FPS),
            menu.ToggleMenuItem('FullScreen:', self.on_full_screen, director.director.window.fullscreen),
            menu.ToggleMenuItem('Run Animations:', self.on_run_animations, C.UI.Cocos.RunAnimations),
            menu.MenuItem('Back', self.on_quit)
        ]

        self.create_menu(items)

        # From which scene to this layer?
        self.where_come_from = None

    @staticmethod
    def on_show_fps(value):
        director.director.show_FPS = bool(value)

    @staticmethod
    def on_full_screen(value):
        director.director.window.set_fullscreen(bool(value))

    @staticmethod
    def on_run_animations(value):
        C.UI.Cocos.RunAnimations = bool(value)

    def on_quit(self):
        if self.where_come_from is None:
            self.parent.switch_to(MainLayer.MainID)
        else:
            main_scene = self.ctrl.get('main')
            if self.where_come_from is main_scene:
                self.parent.switch_to(MainLayer.MainID)
            else:
                director.director.replace(transitions.FadeTransition(self.where_come_from, duration=1.0))


def get_main_scene(controller):
    main_scene = scene.Scene()

    main_scene.add(BackgroundLayer(), z=0, name='background')
    main_scene.add(BasicButtonsLayer(controller, back=False), z=1, name='basic_buttons')
    main_scene.add(MainLayer(
        MainMenu(controller),
        OptionsMenu(controller),
    ), z=2, name='main')

    return main_scene


__all__ = [
    'get_main_scene',
]
