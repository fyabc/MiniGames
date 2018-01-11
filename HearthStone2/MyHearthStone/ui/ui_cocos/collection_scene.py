#! /usr/bin/python
# -*- coding: utf-8 -*-

from cocos import scene, layer
from cocos.director import director
from cocos.scenes import transitions

from .basic_components import BackgroundLayer, BasicButtonsLayer

__author__ = 'fyabc'


class CollectionsLayer(layer.Layer):
    def __init__(self, ctrl):
        super().__init__()
        self.ctrl = ctrl


def get_collection_scene(controller):
    def back_to_main():
        director.replace(transitions.SlideInRTransition(controller.scenes['main'], duration=1.0))

    collection_scene = scene.Scene()
    collection_scene.add(BackgroundLayer(), z=0)
    collection_scene.add(BasicButtonsLayer(back_func=back_to_main), z=1)
    collection_scene.add(CollectionsLayer(controller), z=2)

    return collection_scene


__all__ = [
    'get_collection_scene',
]
