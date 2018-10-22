#! /usr/bin/python
# -*- coding: utf-8 -*-

"""The scene and layers of the world."""

from cocos import layer, scene, actions

from .constants import Colors
from .basic import pos
from .adventurer import Adventurer, get_policy_driver, set_value_policy

__author__ = 'fyabc'


class Background(layer.ColorLayer):
    def __init__(self):
        super().__init__(*Colors['white'])


class World(layer.Layer):
    def __init__(self):
        super().__init__()

        # For debug.
        adventurer = Adventurer(pos(0.5, 0.5))
        self.add(adventurer)
        adventurer.do(get_policy_driver(set_value_policy(rotation=60, speed=100)))


def get_main_scene():
    return scene.Scene(Background(), World())
