#! /usr/bin/python
# -*- encoding: utf-8 -*-

import pygame
import pygame.locals

from ..config import *
from ..element.group import Group
from ..element.shift_elements import Hero, ShiftText
from .scene import Scene
from ..utils.display import update
from ..utils.keymap import get_keymap, get_unique_key_event

__author__ = 'fyabc'


class LevelScene(Scene):
    def __init__(self, game, scene_id, targets):
        super().__init__(game, scene_id, targets)

        self.game_group_name = DefaultGroup
        self.current_level_id = 1

        self.game_group_data = None
        self.level_data = None
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

            # Elements
            self.hero, self.doors, self.traps, self.arrows,
            self.keys, self.lamps, self.blocks, self.mosaics,
            self.texts,

            # kwargs
            ordered=True,
        )

    def _add_keys(self):
        super()._add_keys()

        km = get_keymap()

        for key in km['quit']:
            self.add_action(get_unique_key_event(key),
                            lambda s, *args: (self.targets['LevelSelectMenu'], s.game_group_name))

        for real_key in ('left', 'right', 'jump', 'shift', 'enter'):
            for key in km[real_key]:
                self.add_action(get_unique_key_event(key, is_down=True), self._update_command)

                # Add left stop and right stop
                if real_key in ('left', 'right'):
                    self.add_action(get_unique_key_event(key, is_down=False), self._update_command)

    def _set_group_and_level(self, game_group_name, level_id):
        """Set the game according to the group and level.

        Also set elements.
        """

        self.game_group_name = game_group_name
        self.game_group_data = self.game.game_groups_data[game_group_name]

        self.current_level_id = level_id
        self.level_data = self.game_group_data[level_id]
        self._size = self.level_data.size
        self._cell_width = ScreenWidth // self._size[0]
        self._cell_height = ScreenHeight // self._size[1]

        self._load_elements()

    def physic_loc(self, logic_loc, anchor=Anchor.center):
        lx, ly = logic_loc

        anchor = Anchor.str2anchor(anchor)

        dx, dy = Anchor.LocationMap[anchor]

        return int(self._cell_width * (lx + dx)), int(self._cell_height * (ly + dy))

    def clear_all(self):
        for group in self.groups:
            if hasattr(group, 'clear'):
                group.clear()

    def _load_elements(self, reload=True):
        if reload:
            self.clear_all()

        # For debug
        print('Level data:')
        print(self.level_data)
        # End debug

        pass

    def draw_background(self):
        lx, ly = self._size

        for i in range(lx):
            for j in range(ly):
                self.surface.fill(
                    Bool2Color[self.level_data[i, j]],
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

        # For debug
        print('Args @ level scene:', *args)
        # End debug

        # Set the group and level before running.
        self._set_group_and_level(args[0], args[1])

        return super().run(previous_scene_id, *args)

    # Methods of running command from the user key input.

    @staticmethod
    def _get_command(event):
        km = get_keymap()

        event_key = event.key

        if event.type == pygame.locals.KEYDOWN:
            if event_key in km['left']:
                return 'left'
            elif event_key in km['right']:
                return 'right'
            elif event_key in km['jump']:
                return 'jump'
            elif event_key in km['shift']:
                return 'shift'
            elif event_key in km['enter']:
                return 'enter'
        elif event.type == pygame.locals.KEYUP:
            if event_key in km['left']:
                return 'left_stop'
            elif event_key in km['right']:
                return 'right_stop'
        return 'no_op'

    def _update_command(self, scene, event, previous_scene_id, *args):
        # Parse event to command.
        command = self._get_command(event)

        # If command is 'No Op', just return None.
        if command == 'no_op':
            return

        print('%command =', command)

        # Update the scene by the command.
