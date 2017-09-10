#! /usr/bin/python
# -*- encoding: utf-8 -*-

import os

import pyglet
from cocos import director

from ...core import Game
from .views.main_scene import get_main_scene
from .views.deck_scene import get_deck_scene
from ...utils.io_utils import make_directories, load_decks, save_decks
from .constants import WindowSize

__author__ = 'fyabc'


class Controller(pyglet.event.EventDispatcher):
    """The controller of the game, include all.
    
    The controller is an event dispatcher, so we can send events to it.
    """

    def __init__(self):
        self.running = True

        # Current game core.
        self.game = None

        # Save all decks
        self.decks = []

        self.init()

        # Scenes
        self.main_scene = get_main_scene(self)
        self.deck_scene = get_deck_scene(self)

    def init(self):
        director.director.init(
            caption='HearthStone',
            resizable=True,
            width=WindowSize[0],
            height=WindowSize[1],
        )

        make_directories()
        self.decks = load_decks()

    def on_quit(self):
        """Do something on quit, such as save decks."""

        if not self.running:
            return

        print('Quitting game...')

        save_decks(self.decks)

        pyglet.app.exit()

        self.running = False

    def run(self):
        director.director.run_after(self.main_scene)

        self.on_quit()
