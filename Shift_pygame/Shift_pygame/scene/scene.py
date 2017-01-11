#! /usr/bin/python
# -*- coding: utf-8 -*-

from ..utils.display import update

__author__ = 'fyabc'


class Scene:
    def __init__(self, game, data=None):
        self.game = game
        self.data = data

    def register_to_game(self):
        scene_id = self.data['id']

        self.game.scenes[scene_id] = self

    def run(self, previous_scene_id, *args):
        next_scene_id = None

        while True:
            update()

        return next_scene_id

    def draw(self):
        pass
