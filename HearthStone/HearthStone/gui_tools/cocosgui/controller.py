#! /usr/bin/python
# -*- encoding: utf-8 -*-

__author__ = 'fyabc'


class Controller:
    """The controller of the game (MVC pattern)."""

    def __init__(self, game):
        self.game = game

        # Save all decks
        self.decks = []

    def on_quit(self):
        """Do something on quit, such as save decks."""
        pass
