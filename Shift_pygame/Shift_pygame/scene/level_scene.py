#! /usr/bin/python
# -*- encoding: utf-8 -*-

from ..config import *
from ..element.group import Group
from ..element.shift_elements import Hero, ShiftText
from .scene import Scene
from ..utils.display import update

__author__ = 'fyabc'


class LevelScene(Scene):
    def __init__(self, game, scene_id):
        super().__init__(game, scene_id)

        self._game_group_name = DefaultGroup
        self._current_level_id = 1

        self._game_group_data = None
        self._level_data = None
        self._size = None
        self._cell_width = None
        self._cell_height = None

        self.hero = Group(self.game)
        self.doors = Group(self.game)
        self.traps = Group(self.game)
        self.arrows = Group(self.game)
        self.keys = Group(self.game)
        self.blocks = Group(self.game)
        self.lamps = Group(self.game)
        self.mosaics = Group(self.game)
        self.texts = Group(self.game)

        self.groups = Group(
            self.game,
            self.hero, self.doors, self.traps, self.arrows,
            self.keys, self.lamps, self.blocks, self.mosaics,
            self.texts,
            ordered=True,
        )

    def _set_group_and_level(self, game_group_name, level_id):
        self._game_group_name = game_group_name
        self._game_group_data = self.game.game_groups_data[game_group_name]

        self._current_level_id = level_id
        self._level_data = self._game_group_data[level_id]
        self._size = self._level_data.size
        self._cell_width = ScreenWidth // self._size[0]
        self._cell_height = ScreenHeight // self._size[1]

        self.load_elements()

    def physic_loc(self, logic_loc, anchor=Anchor.center):
        lx, ly = logic_loc

        if isinstance(anchor, str):
            anchor = eval('Anchor.' + anchor)

        if anchor == Anchor.center:
            return self._cell_width * lx + self._cell_width // 2, self._cell_height * ly + self._cell_height // 2
        else:
            raise ValueError('Does not support anchor {}'.format(anchor))

    def clear_all(self):
        for group in self.groups:
            if hasattr(group, 'clear'):
                group.clear()

    def load_elements(self, reload=True):
        if reload:
            self.clear_all()

        pass

    def draw_background(self):
        lx, ly = self._size

        for i in range(lx):
            for j in range(ly):
                self.surface.fill(
                    Bool2Color[self._level_data[i, j]],
                    pygame.Rect(i * self._cell_width, j * self._cell_height, self._cell_width, self._cell_height)
                )

        update()

    def run(self, previous_scene_id, *args):
        """

        :param previous_scene_id:
        :param args:
            args[0]: game_group_name
            args[1]: level_id
        :return:
        """

        # Set the group and level before running.
        self._set_group_and_level(args[0], args[1])

        return super().run(previous_scene_id, *args)
