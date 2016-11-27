#! /usr/bin/python
# -*- coding: utf-8 -*-
from HearthStone.event_framework import Handler

__author__ = 'fyabc'


class GameHandler(Handler):
    def __init__(self, game):
        super(GameHandler, self).__init__()
        self.game = game
