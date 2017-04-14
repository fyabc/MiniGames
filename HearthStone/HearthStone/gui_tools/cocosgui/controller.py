#! /usr/bin/python
# -*- encoding: utf-8 -*-

from cocos import director

from ...core import Game
from .views.main_scene import get_main_scene

__author__ = 'fyabc'


class Controller:
    """The controller of the game, include all."""

    def __init__(self):
        director.director.init(
            caption='HearthStone',
            resizable=True,
            width=800,
            height=600,
        )

        # Current game core.
        self.game = None

        # Scenes
        self.main_scene = get_main_scene(self)

        # Save all decks
        self.decks = []

    def on_quit(self):
        """Do something on quit, such as save decks."""
        pass

    def run(self):
        director.director.run(self.main_scene)
