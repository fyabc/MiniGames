#! /usr/bin/python
# -*- encoding: utf-8 -*-

from ..config import *
from ..element.group import Group
from .scene import Scene
from ..utils.display import update
from ..utils.data_parser import load_game_group

__author__ = 'fyabc'


class LevelScene(Scene):
    def __init__(self, game, game_map):
        super().__init__(game, game_map['id'])
        self.map = game_map['map']

        size = self.map.size

        self.cell_width = ScreenWidth // size[0]
        self.cell_height = ScreenHeight // size[1]

        self.hero = None
        self.doors = Group(self.game)
        self.traps = Group(self.game)
        self.arrows = Group(self.game)
        self.keys = Group(self.game)
        self.blocks = Group(self.game)
        self.lamps = Group(self.game)
        self.mosaics = Group(self.game)

        self.groups = [
            self.hero, self.doors, self.traps, self.arrows,
            self.keys, self.blocks, self.lamps, self.mosaics,
        ]

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

    def draw_background(self):
        lx, ly = self.map.size

        for i in range(lx):
            for j in range(ly):
                self.surface.fill(
                    Bool2Color[self.map[i, j]],
                    pygame.Rect(i * self.cell_width, j * self.cell_height, self.cell_width, self.cell_height)
                )

        for s_obj in self.static_objects:
            s_obj.draw()

        update()
