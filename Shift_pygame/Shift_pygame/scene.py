#! /usr/bin/python
# -*- coding: utf-8 -*-

from .utils.display import update

__author__ = 'fyabc'


class Scene:
    def run(self, previous_scene_id, *args):
        next_scene_id = None

        while True:
            update()

        return next_scene_id, *args
