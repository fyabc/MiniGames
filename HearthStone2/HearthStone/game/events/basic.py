#! /usr/bin/python
# -*- coding: utf-8 -*-

from ...utils.message import message
from .event import Event

__author__ = 'fyabc'


class BeginOfTurn(Event):
    check_win_after = True

    def __init__(self, game):
        super().__init__(game, None)

    def message(self):
        message('Turn {} begin, player = {}'.format(self.game.n_turns, self.game.current_player))


class EndOfTurn(Event):
    check_win_after = True

    def __init__(self, game):
        super().__init__(game, None)

    def message(self):
        message('Turn {} end, player = {}'.format(self.game.n_turns, self.game.current_player))

    def run(self):
        super().run()

        self.game.end_turn()


class DrawCard(Event):
    pass
