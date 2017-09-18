#! /usr/bin/python
# -*- coding: utf-8 -*-

"""Standard events."""

from .event import Event
from .play import *
from .damage import *
from .death import *
from .combat import *
from .hero_power import *

__author__ = 'fyabc'


class BeginOfGame(Event):
    def __init__(self, game):
        super().__init__(game, game)

    def message(self):
        super().message(first_player=self.game.current_player)


class BeginOfTurn(Event):
    def __init__(self, game):
        super().__init__(game, game)

    def message(self):
        super().message(n=self.game.n_turns, player=self.game.current_player)


class EndOfTurn(Event):
    def __init__(self, game):
        super().__init__(game, game)

    def message(self):
        super().message(n=self.game.n_turns, player=self.game.current_player)


class DrawCard(Event):
    def __init__(self, game, owner, player_id=None):
        super().__init__(game, owner)
        self.player_id = player_id if player_id is not None else self.game.current_player
        self.card = None

    def message(self):
        super().message(P=self.player_id, card=self.card)


def game_begin_standard_events(game):
    return [BeginOfGame(game), BeginOfTurn(game), DrawCard(game, None)]
