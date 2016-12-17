#! /usr/bin/python
# -*- coding: utf-8 -*-

from ..constants import Location_DESK
from .game_handler import GameHandler

__author__ = 'fyabc'


class CardHandler(GameHandler):
    """Handlers of card.

    The owner of the handler must be a card.

    It will be created by cards as their skills.
    It will be connect to the location of cards.
    """

    # The locations where this kind of handlers will be enable.
    enable_locations = []

    def __init__(self, game, owner=None):
        super().__init__(game, owner)

    def trigger(self, old_location, new_location):
        """Method that called by owner when the owner change its location.

        This method should be called in owner's `change_location` method.
        """

        old_in = old_location in self.enable_locations
        new_in = new_location in self.enable_locations

        if old_in and not new_in:
            self.disable()

        if new_in and not old_in:
            self.game.engine.add_handler(self)


class DeskHandler(CardHandler):
    """The most common used handler type, that enable only in desk."""

    enable_locations = [Location_DESK]


__all__ = [
    'CardHandler',
    'DeskHandler',
]
