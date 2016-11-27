#! /usr/bin/python
# -*- coding: utf-8 -*-
from HearthStone.event_framework import Handler

__author__ = 'fyabc'


class GameHandler(Handler):
    def __init__(self, game):
        super(GameHandler, self).__init__()
        self.game = game

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


__all__ = [
    'GameHandler',
]
