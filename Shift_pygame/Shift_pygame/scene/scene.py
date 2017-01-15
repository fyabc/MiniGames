#! /usr/bin/python
# -*- coding: utf-8 -*-

import pygame
import pygame.locals

from ..config import *
from ..utils.keymap import get_keymap, get_unique_key_event
from ..utils.display import update
from ..handler.handler import EventHandler
from ..element.group import Group

__author__ = 'fyabc'


class Scene(EventHandler):
    QuitID = QuitID

    def __init__(self, game, scene_id=None):
        super().__init__(game)
        self.surface = self.game.main_window
        self.scene_id = scene_id

        self.handlers = []
        self.background_group = Group(self.game)

        self.groups = [self.background_group]

        # The default exit action.
        self.add_jump_action(pygame.locals.QUIT, self.QuitID)

        self._add_keys()

    def _add_keys(self):
        km = get_keymap()

        for key in km['exit']:
            self.add_jump_action(get_unique_key_event(key), self.QuitID)

    def register_to_game(self):
        self.game.scenes[self.scene_id] = self

    def add_background(self, *elements):
        self.background_group.add(*elements)

    def run(self, previous_scene_id, *args):
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

            self.draw()

    def draw_background(self):
        self.surface.fill(BackgroundColor)

    def draw(self, ud=True, bg=False):
        if bg:
            self.draw_background()

        for group in self.groups:
            group.draw()

        if ud:
            update()
