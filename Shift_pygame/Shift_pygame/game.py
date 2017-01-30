#! /usr/bin/python
# -*- coding: utf-8 -*-

import sys
from contextlib import contextmanager

import pygame
import pygame.locals

from .config import *
from .utils.display import get_font
from .group_data import GameGroupData
from .scene.basic_scenes import *
from .scene.level_scene import LevelScene

__author__ = 'fyabc'


class Game:
    def __init__(self):
        # Initialize pygame.
        pygame.init()
        self.main_window = pygame.display.set_mode(WindowSize)
        self.timer = pygame.time.Clock()
        self.gFont = get_font()

        pygame.display.set_caption(GameTitle)

        # Game initialize.
        self.previous_scene_id = None
        self.current_scene_id = 0
        self.args_between_scenes = []
        self.scenes = {}

        # Data initialize.
        self.game_groups_data = GameGroupData.load_game_groups()

        self.scene_map = {}

        self._register_scene(
            MainMenu,
            HelpMenu,
            GameSelectMenu,
            GameMainMenu,
            LevelSelectMenu,
            LevelScene,
        )

        self._construct_scene(MainMenu, self.scene_map)
        self._construct_scene(HelpMenu, self.scene_map)
        self._construct_scene(GameSelectMenu, self.scene_map)
        self._construct_scene(GameMainMenu, self.scene_map)
        self._construct_scene(LevelSelectMenu, self.scene_map)
        self._construct_scene(LevelScene, self.scene_map)

    @contextmanager
    def _game_manager(self):
        # This may be speed up the game or not?
        pygame.event.set_allowed([
            pygame.locals.KEYDOWN,
            pygame.locals.KEYUP,
            pygame.locals.MOUSEBUTTONDOWN,
            pygame.locals.MOUSEBUTTONUP,
        ])

        yield

        pygame.quit()

        # Save some data of the game.
        print('Saving game status... ', end='')
        for game_group_data in self.game_groups_data.values():
            game_group_data.dump_game_group()
        print('done')

        print('The game is quited!')
        sys.exit(0)

    def _register_scene(self, *scene_types):
        self.scene_map = {}
        for i, scene_type in enumerate(scene_types):
            self.scene_map[scene_type.__name__] = i

    def _construct_scene(self, scene_type, *args, **kwargs):
        scene_id = self.scene_map[scene_type.__name__]
        self.scenes[scene_id] = scene_type(self, scene_id, *args, **kwargs)

    def run(self):
        with self._game_manager():
            while True:
                scene = self.scenes[self.current_scene_id]

                result = scene.run(self.previous_scene_id, *self.args_between_scenes)

                if hasattr(result, '__len__'):
                    next_scene_id, *self.args_between_scenes = result
                else:
                    next_scene_id = result
                    self.args_between_scenes = []

                if next_scene_id == MainMenu.QuitID:
                    break

                self.previous_scene_id, self.current_scene_id = self.current_scene_id, next_scene_id
