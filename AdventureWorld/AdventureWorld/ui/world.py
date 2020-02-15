#! /usr/bin/python
# -*- coding: utf-8 -*-

"""The scene and layers of the world."""

from cocos import layer, scene

from .constants import Colors
from .basic import pos
from .adventurer import Adventurer

__author__ = 'fyabc'


class Background(layer.ColorLayer):
    def __init__(self):
        super().__init__(*Colors['white'])


class World(layer.Layer):
    def __init__(self):
        super().__init__()

        self.debug_fn()

    def debug_fn(self):
        from .adventurer import policies2action
        from ..controller.policies import p_set_value, p_circle, p_shoot_bullet

        def _add_sprite(position, policy_list):
            adventurer = Adventurer(pos(*position))
            self.add(adventurer)
            adventurer.do(policies2action(policy_list))

        _add_sprite((0.2, 0.3), [p_set_value(rotation=60, speed=70)])
        _add_sprite((0.2, 0.8), [p_circle(speed=60, start_theta=90, d_theta=40), p_shoot_bullet(duration=1)])


def get_main_scene():
    return scene.Scene(Background(), World())
