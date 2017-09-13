#! /usr/bin/python
# -*- coding: utf-8 -*-

from ...utils.message import message
from .event import Event

__author__ = 'fyabc'


class BeginOfGame(Event):
    def __init__(self, game):
        super().__init__(game, None)
        self._oop = game.inc_oop()

    @property
    def oop(self):
        return self._oop

    def message(self):
        super().message(first_player=self.game.current_player)


class BeginOfTurn(Event):
    def __init__(self, game):
        super().__init__(game, None)
        self._oop = game.inc_oop()

    @property
    def oop(self):
        return self._oop

    def message(self):
        super().message(n=self.game.n_turns, player=self.game.current_player)


class EndOfTurn(Event):
    def __init__(self, game):
        super().__init__(game, None)
        self._oop = game.inc_oop()

    @property
    def oop(self):
        return self._oop

    def message(self):
        super().message(n=self.game.n_turns, player=self.game.current_player)

    def run_after(self):
        super().run_after()

        self.game.end_turn()


class DrawCard(Event):
    def __init__(self, game, owner, player_id):
        super().__init__(game, owner)
        self.player_id = player_id
        self.card = None

    def message(self):
        super().message(player=self.game.current_player, card=self.card)

    def run_before(self):
        # todo
        pass
