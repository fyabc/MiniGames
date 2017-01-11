#! /usr/bin/python
# -*- coding: utf-8 -*-

import sys
from contextlib import contextmanager

import pygame

from .config import *
from .scene.basic_scenes import MainMenu

__author__ = 'fyabc'


class Game:
    def __init__(self):
        # Initialize pygame.
        pygame.init()
        self.main_window = pygame.display.set_mode(WindowSize)
        pygame.display.set_caption(GameTitle)

        # Game initialize.
        self.previous_scene_id = None
        self.current_scene_id = 0
        self.args_between_scenes = []
        self.scenes = {}

        self.add_scene(0, MainMenu)

    @contextmanager
    def _game_manager(self):
        yield

        pygame.quit()

        # Save some data of the game.

        print('The game is quited!')
        sys.exit(0)

    def add_scene(self, scene_id, scene_type, *args, **kwargs):
        self.scenes[scene_id] = scene_type(self, scene_id, *args, **kwargs)

    def run(self):
        with self._game_manager():
            while True:
                scene = self.scenes[self.current_scene_id]

                next_scene_id, *self.args_between_scenes = scene.run(self.previous_scene_id, *self.args_between_scenes)

                self.previous_scene_id, self.current_scene_id = self.current_scene_id, next_scene_id
