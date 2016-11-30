#! /usr/bin/python
# -*- coding: utf-8 -*-

from HearthStone.event_framework import Handler
from HearthStone.game_event import *

__author__ = 'fyabc'


class GameHandler(Handler):
    def __init__(self, game, owner=None):
        """The base class of game handlers.
        [NOTE] The first parameter of `__init__` for `GameHandler`'s subclasses must be `game`.

        :param game: The game of this handler.
        :param owner: The owner of this handler.
            The handler can send some information or signals (such as terminate) to its owner.
        """

        super(GameHandler, self).__init__()
        self.game = game
        self.owner = owner

    # [NOTE] This method is just for test.
    def __str__(self):
        return '{}#{}(alive={},event_types={})'.format(
            self.__class__.__name__,
            self.id,
            self.alive,
            [event_type.__name__ for event_type in self.event_types],
        )

    def _process(self, event):
        print('{} is processing {}!'.format(self, event))


class TurnBeginDrawCardHandler(GameHandler):
    """The default handler of `TurnBegin`.

    It will draw a card for current player.
    """

    event_types = [TurnBegin]

    def _process(self, event):
        self.game.add_event_quick(DrawCard)


__all__ = [
    'GameHandler',
    'TurnBeginDrawCardHandler',
]
