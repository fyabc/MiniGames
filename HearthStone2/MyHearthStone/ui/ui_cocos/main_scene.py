#! /usr/bin/python
# -*- coding: utf-8 -*-

"""The main scene of the cocos-single frontend.

This is one of the views in MVC pattern.
"""

# TODO: Copy from old HearthStone project now, need more fix.

from cocos import director, layer, scene, menu
from cocos.scenes import transitions
import pyglet

from .utils import set_menu_style
from .background_layer import BackgroundLayer

from ...utils.constants import C

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

        # TODO: start a new game.

    def on_deck(self):
        director.director.replace(transitions.SlideInLTransition(self.ctrl.scenes['collection'], duration=1.2))

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

        self.create_menu(
            items,
            selected_effect=menu.shake(),
            unselected_effect=menu.shake_back(),
        )

    @staticmethod
    def on_show_fps(value):
        director.director.show_FPS = bool(value)

    @staticmethod
    def on_full_screen():
        director.window.set_fullscreen(not director.window.fullscreen)

    def on_quit(self):
        self.parent.switch_to(0)


def get_main_scene(controller):
    main_scene = scene.Scene()

    main_scene.add(BackgroundLayer(), z=0)
    main_scene.add(layer.MultiplexLayer(
        MainMenu(controller),
        OptionsMenu(controller),
    ), z=1)

    return main_scene


__all__ = [
    'get_main_scene',
]
