#! /usr/bin/python
# -*- coding: utf-8 -*-

from ...utils.message import message
from .event import Event

__author__ = 'fyabc'


class BeginOfTurn(Event):
    def __init__(self, game):
        super().__init__(game, None)
        self._oop = game.inc_oop()

    @property
    def oop(self):
        return self._oop

    def message(self):
        message('Turn {} begin, player = {}'.format(self.game.n_turns, self.game.current_player))


class EndOfTurn(Event):
    def __init__(self, game):
        super().__init__(game, None)
        self._oop = game.inc_oop()

    @property
    def oop(self):
        return self._oop

    def message(self):
        message('Turn {} end, player = {}'.format(self.game.n_turns, self.game.current_player))

    def run(self):
        super().run()

        self.game.end_turn()


class DrawCard(Event):
    pass
