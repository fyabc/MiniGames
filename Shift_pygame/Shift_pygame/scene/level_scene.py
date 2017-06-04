#! /usr/bin/python
# -*- encoding: utf-8 -*-

import pygame
import pygame.locals

from ..config import *
from ..element.group import Group
from ..element.shift_elements import Hero, Door, Trap, ShiftText
from .scene import Scene
from ..utils.keymap import get_keymap, get_unique_key_event
from ..support import Vector2

__author__ = 'fyabc'


class LevelScene(Scene):
    def __init__(self, game, scene_id, targets):
        super().__init__(game, scene_id, targets)

        self.game_group_name = DefaultGroup
        self.current_level_id = 1

        self.game_group_data = None
        self.level_data = None
        self._size = None
        self.cell_width = None
        self.cell_height = None
        self._angle = 0

        # [NOTE] The heroes will only contains a single hero (`self.hero`).
        self.heroes = Group(self.game, ordered=True)
        self.doors = Group(self.game)
        self.traps = Group(self.game)
        self.arrows = Group(self.game)
        self.keys = Group(self.game)
        self.blocks = Group(self.game)
        self.lamps = Group(self.game)
        self.mosaics = Group(self.game)
        self.texts = Group(self.game)

        self.hero = None

        self.groups = Group(
            self.game,

            # Elements
            self.heroes, self.doors, self.traps, self.arrows,
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

    # Some utilities for elements.

    def physic_loc(self, logic_loc, anchor=Anchor.center):
        """Get physic location with given logic location and anchor."""

        lx, ly = logic_loc

        anchor = Anchor.str2anchor(anchor)

        dx, dy = Anchor.LocationMap[anchor]

        return Vector2(self.cell_width * (lx + dx), self.cell_height * (ly + dy))

    def logic_loc(self, loc, strict=True):
        result = loc[0] // self.cell_width, loc[1] // self.cell_height

        if not strict:
            return result

        if not (0 <= result[0] < self._size[0] and 0 <= result[1] < self._size[1]):
            return None

        # Add check for blocks and mosaics

        return result

    def get_color(self, x, y):
        """Get boolean color."""
        return self.level_data[self.rotated_location(x, y)]

    # Methods for setting data, loading elements or others.

    def _set_group_and_level(self, game_group_name, level_id):
        """Set the game according to the group and level.

        Also set elements.
        """

        self.game_group_name = game_group_name
        self.game_group_data = self.game.game_groups_data[game_group_name]

        self.current_level_id = level_id
        self.level_data = self.game_group_data[level_id]
        self._size = self.level_data.size
        self.cell_width = ScreenWidth // self._size[0]
        self.cell_height = ScreenHeight // self._size[1]

        self._load_elements()

    def clear_all(self):
        for group in self.groups:
            if hasattr(group, 'clear'):
                group.clear()

    def _load_elements(self, reload=True):
        if reload:
            self.clear_all()

        # # For debug
        # print('Level data:')
        # print(self.level_data)
        # # End debug

        elements = self.level_data.elements

        self.doors.add(*(
            Door.from_attributes(self.game, self, attributes)
            for attributes in elements['door'].values()
        ))

        self.traps.add(*(
            Trap.from_attributes(self.game, self, attributes)
            for attributes in elements['trap'].values()
        ))

        self.heroes.add(*(
            Hero.from_attributes(self.game, self, attributes)
            for attributes in elements['start'].values()
        ))

        # Set the hero (the first hero of heroes)
        self.hero = self.heroes[0]

    def draw_background(self):
        lx, ly = self._size

        for i in range(lx):
            for j in range(ly):
                self.surface.fill(
                    Bool2Color[self.get_color(i, j)],
                    pygame.Rect(i * self.cell_width, j * self.cell_height, self.cell_width, self.cell_height)
                )

    def draw(self, ud=True, bg=True):
        super().draw(ud=ud, bg=bg)

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

        self.draw_background()

        while True:
            self.game.timer.tick(MainFPS)

            for event in pygame.event.get():
                pos = getattr(event, 'pos', None)
                overridden = False

                if pos is not None:
                    # Handlers which contains the position
                    for handler in self.handlers:
                        if pos in handler:
                            result = handler.process(event, previous_scene_id, *args)
                            if result is not None:
                                return result
                            if handler.override(event):
                                overridden = True
                                break

                if not overridden:
                    result = self.process(event, previous_scene_id, *args)
                    if result is not None:
                        return result

            result = self.update(MainFPS)

            self.draw()

            # Test result.
            if result is not None:
                if result >= 0:
                    # Win, result is next level ID
                    pass
                else:
                    # Lose
                    pass

    def update(self, fps):
        self.hero.update(fps)

        return None

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

        # Update the scene by the command.
        self.hero.run_command(command)

    def rotated_location(self, x, y, angle=None):
        if angle is None:
            angle = self._angle

        if angle == 0:
            return x, y
        elif angle == 90:
            return self._size[1] - 1 - y, x
        elif angle == 180:
            return self._size[0] - 1 - x, self._size[1] - 1 - y
        elif angle == 270:
            return y, self._size[0] - 1 - x

    def _do_rotate(self, angle):
        self._angle = (self._angle + angle + 360) % 360

        # Change angles of group elements.
        for group in self.groups:
            for element in group:
                element.rotate_window(angle)

    def rotate_map(self, angle):
        # todo: add rotate animation here
        self._do_rotate(angle)

    def shift_map(self):
        # todo: add shift animation and hero change here
        self._do_rotate(180)
