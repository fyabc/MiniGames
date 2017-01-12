#! /usr/bin/python
# -*- encoding: utf-8 -*-

from ..config import *
from .scene import Scene
from ..utils.data_parser import load_game_group

__author__ = 'fyabc'


class LevelScene(Scene):
    def __init__(self, game, game_map):
        super().__init__(game, game_map['id'])
        self.map = game_map['map']

        size = self.map.size

        self.cell_width = ScreenWidth // size[0]
        self.cell_height = ScreenHeight // size[1]

    @classmethod
    def from_game_group(cls, game, game_group_name):
        result = load_game_group(game_group_name)

        return [cls(game, data) for data in result]

    def physic_loc(self, logic_loc, anchor='center'):
        lx, ly = logic_loc

        if anchor == 'center':
            return self.cell_width * lx + self.cell_width // 2, self.cell_height * ly + self.cell_height // 2
        else:
            raise ValueError('Does not support anchor "{}"'.format(anchor))
