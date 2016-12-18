#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'fyabc'


class GameEntity:
    """The base class of game entities.

    a GameEntity object connect to a Game instance.
    a GameEntity object have some handlers registered to the engine of its game.
    """

    def __init__(self, game):
        self.game = game
        self.handlers = set()

    def disable_all_handlers(self):
        for handler in self.handlers:
            handler.disable()

    def add_handler_quick(self, handler_type):
        self.handlers.add(handler_type(self.game, self))


__all__ = [
    'GameEntity',
]
