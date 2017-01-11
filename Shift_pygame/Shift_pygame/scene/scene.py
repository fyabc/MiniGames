#! /usr/bin/python
# -*- coding: utf-8 -*-

from ..utils.display import update

__author__ = 'fyabc'


class Scene:
    def __init__(self, game, scene_id=None):
        self.game = game
        self.scene_id = scene_id

    def register_to_game(self):
        self.game.scenes[self.scene_id] = self

    def run(self, previous_scene_id, *args):
        next_scene_id = None

        while True:
            update()

        return next_scene_id

    def draw(self):
        pass
