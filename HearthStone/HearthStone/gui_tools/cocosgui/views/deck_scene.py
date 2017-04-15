#! /usr/bin/python
# -*- encoding: utf-8 -*-

from cocos import scene, layer, menu
from cocos.director import director
from cocos.scenes import transitions

from ..utils import set_menu_style, abs_pos

__author__ = 'fyabc'


class CardsLayer(layer.Layer):
    """Layer that show cards."""

    def __init__(self, controller):
        super().__init__()
        self.ctrl = controller


class DeckMenu(menu.Menu):
    """Deck menu."""

    def __init__(self, controller):
        super().__init__('Deck')

        self.ctrl = controller

        set_menu_style(self, item_size=24)

        window_size = director.get_window_size()

        items = [
            menu.MenuItem('Back', self.on_quit),
        ]
        items_positions = [
            abs_pos(0.95, 0.05, window_size),
        ]

        self.create_menu(
            items,
            selected_effect=menu.shake(),
            unselected_effect=menu.shake_back(),
            layout_strategy=menu.fixedPositionMenuLayout(items_positions),
        )

    def on_quit(self):
        director.replace(transitions.SlideInRTransition(self.ctrl.main_scene, duration=1.2))


def get_deck_scene(controller):
    deck_scene = scene.Scene()

    deck_scene.add(DeckMenu(controller))
    deck_scene.add(CardsLayer(controller))

    return deck_scene
