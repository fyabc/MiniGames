#! /usr/bin/python
# -*- coding: utf-8 -*-

from cocos import scene, layer

from ...utils.draw.cocos_utils.active import ActiveLayer
from ...utils.draw.cocos_utils.layers import BackgroundLayer, BasicButtonsLayer

__author__ = 'fyabc'


class CollectionsLayer(ActiveLayer):
    def __init__(self, ctrl):
        super().__init__(ctrl)


class DeckSelectLayer(ActiveLayer):
    def __init__(self, ctrl):
        super().__init__(ctrl)

    def on_select_deck(self, deck_id):
        self.parent.layers[1].deck_id = deck_id
        self.parent.switch_to(1)


class DeckEditLayer(ActiveLayer):
    def __init__(self, ctrl):
        super().__init__(ctrl)
        self.deck_id = None

    def on_edit_done(self):
        self.parent.switch_to(0)


def get_collection_scene(controller):
    collection_scene = scene.Scene()
    collection_scene.add(BackgroundLayer(), z=0, name='background')
    collection_scene.add(BasicButtonsLayer(controller), z=1, name='basic_buttons')
    collection_scene.add(CollectionsLayer(controller), z=2, name='collections')
    collection_scene.add(layer.MultiplexLayer(
        DeckSelectLayer(controller),
        DeckEditLayer(controller),
    ), z=3, name='deck')

    return collection_scene


__all__ = [
    'get_collection_scene',
]
