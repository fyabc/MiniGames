#! /usr/bin/python
# -*- coding: utf-8 -*-

from ..utils.debug import verbose

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
        verbose('Handlers of {} are disabled!'.format(self))

        for handler in self.handlers:
            handler.disable()

    def add_handler_quick(self, handler_type, *args, **kwargs):
        self.handlers.add(handler_type(self.game, self, *args, **kwargs))

    def add_handler_inplace(self, handler_type, *args, **kwargs):
        """Add the handler and enable it inplace."""
        new_handler = handler_type(self.game, self, *args, **kwargs)
        self.game.add_handler(new_handler)
        self.handlers.add(new_handler)


__all__ = [
    'GameEntity',
]
