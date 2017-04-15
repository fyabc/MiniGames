#! /usr/bin/python
# -*- coding: utf-8 -*-

"""Game views."""

import pyglet
import cocos
from cocos import layer, text, scene, menu, actions
from cocos.scenes import transitions
from cocos.director import director

from ..constants import Colors, DefaultFont
from ..utils import set_menu_style

__author__ = 'fyabc'


class BackgroundLayer(layer.Layer):
    def __init__(self):
        super(BackgroundLayer, self).__init__()

        # Add more other things here


# todo: OptionsMenu


class OptionsMenu(menu.Menu):
    """Options menu. Index in parent: 1"""

    def __init__(self, controller):
        super().__init__('Options')
        self.ctrl = controller

        set_menu_style(self)

        items = [
            menu.ToggleMenuItem('Show FPS:', self.on_show_fps, director.show_FPS),
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
        director.show_FPS = value

    @staticmethod
    def on_full_screen():
        director.window.set_fullscreen(not director.window.fullscreen)

    def on_quit(self):
        self.parent.switch_to(0)


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

        # todo start a new game.

    def on_deck(self):
        print('Deck!')

        director.push(transitions.FlipAngular3DTransition(self.ctrl.deck_scene, duration=1.5))

    def on_options(self):
        self.parent.switch_to(1)

    def on_quit(self):
        """On key ESCAPE."""

        self.ctrl.on_quit()


def get_main_scene(controller):
    main_scene = scene.Scene()

    main_scene.add(layer.MultiplexLayer(
        MainMenu(controller),
        OptionsMenu(controller),
    ), z=1)
    main_scene.add(BackgroundLayer(), z=0)

    return main_scene
