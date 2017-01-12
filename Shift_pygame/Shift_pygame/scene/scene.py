#! /usr/bin/python
# -*- coding: utf-8 -*-

import pygame
import pygame.locals

from ..config import *
from ..utils.keymap import get_keymap
from ..utils.display import update
from ..handler import EventHandler

__author__ = 'fyabc'


class Scene(EventHandler):
    QuitID = -1

    def __init__(self, game, scene_id=None):
        super().__init__(game)
        self.surface = self.game.main_window
        self.scene_id = scene_id

        self.handlers = []
        self.groups = []

        # The default exit action.
        self.add_action(pygame.locals.QUIT, lambda g, e: self.QuitID)

        self._add_keys()

    def _add_keys(self):
        km = get_keymap()

        for key in km['exit']:
            self.add_action((pygame.locals.KEYDOWN, key), lambda g, e: self.QuitID)

    def register_to_game(self):
        self.game.scenes[self.scene_id] = self

    def run(self, previous_scene_id, *args):
        self.draw_background()

        while True:
            self.game.timer.tick(MainFPS)

            for event in pygame.event.get():
                pos = getattr(event, 'pos', None)

                overrided = False

                if pos is not None:
                    # Elements which contents
                    for handler in self.handlers:
                        if pos in handler:
                            result = handler.process(event)
                            if result is not None:
                                return result
                            if handler.override:
                                overrided = True
                                break

                if not overrided:
                    result = self.process(event)
                    if result is not None:
                        return result

            self.draw()
            update()

    def draw_background(self, bg_color=BackgroundColor):
        self.surface.fill(bg_color)
        update()

    def draw(self):
        for group in self.groups:
            group.draw()