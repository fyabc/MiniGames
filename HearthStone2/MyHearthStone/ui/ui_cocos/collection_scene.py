#! /usr/bin/python
# -*- coding: utf-8 -*-

from cocos import scene, layer
from cocos.director import director
from cocos.scenes import transitions

from .basic_components import BackgroundLayer

__author__ = 'fyabc'


class CollectionsLayer(layer.Layer):
    def __init__(self, ctrl):
        super().__init__()
        self.ctrl = ctrl


def get_collection_scene(controller):
    def back_to_main():
        director.replace(transitions.SlideInRTransition(controller.scenes['collection'], duration=1.0))

    collection_scene = scene.Scene()
    collection_scene.add(BackgroundLayer(back_label_func=back_to_main), z=0)
    collection_scene.add(CollectionsLayer(controller), z=1)

    return collection_scene


__all__ = [
    'get_collection_scene',
]
