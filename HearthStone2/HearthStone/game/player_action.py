#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'fyabc'


class PlayerAction:
    """"""

    def __init__(self, game):
        self.game = game

    def phrases(self):
        """Extract phrases from this player action."""

        raise NotImplementedError('implemented by subclasses')
