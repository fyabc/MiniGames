#! /usr/bin/python
# -*- coding: utf-8 -*-

from .scene import Scene

__author__ = 'fyabc'


class MainMenu(Scene):
    def __init__(self, game, scene_id):
        super().__init__(game, scene_id)
