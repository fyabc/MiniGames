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


class TurnEndDefaultHandler(GameHandler):
    """The default handler of `TurnEnd`, push a `TurnBegin` event."""

    event_types = [TurnEnd]

    def __init__(self, game):
        super(TurnEndDefaultHandler, self).__init__(game, None)

    def _process(self, event):
        super()._process(event)
        self.game.next_turn()
        self.game.add_events(self.game.create_event(TurnBegin))


__all__ = [
    'GameHandler',
    'TurnEndDefaultHandler',
]
