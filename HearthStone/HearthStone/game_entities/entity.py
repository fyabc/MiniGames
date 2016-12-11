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
        self.handlers = {}

    def kill_self(self):
        for handler in self.handlers:
            handler.kill()


__all__ = [
    'GameEntity',
]
