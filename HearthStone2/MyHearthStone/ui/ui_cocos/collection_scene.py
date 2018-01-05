#! /usr/bin/python
# -*- coding: utf-8 -*-

from cocos import scene

from .background_layer import BackgroundLayer

__author__ = 'fyabc'


def get_collection_scene(controller):
    collection_scene = scene.Scene()
    collection_scene.add(BackgroundLayer(), z=0)

    return collection_scene


__all__ = [
    'get_collection_scene',
]
