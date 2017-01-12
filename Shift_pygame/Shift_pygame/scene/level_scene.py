#! /usr/bin/python
# -*- encoding: utf-8 -*-

from .scene import Scene
from ..utils.data_parser import load_game_group

__author__ = 'fyabc'


class LevelScene(Scene):
    def __init__(self, game, scene_id, game_map):
        super().__init__(game, scene_id)
        self.map = game_map

    @classmethod
    def from_game_group(cls, game, game_group_name):
        result = load_game_group(game_group_name)

        return [cls(game, data) for data in result]
