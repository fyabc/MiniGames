#! /usr/bin/python
# -*- coding: utf-8 -*-

"""This module include all standard events."""

from .event import Event
from .play import *
from .damage import *
from .death import *
from .combat import *
from .hero_power import *
from .misc import *
from .utils import dynamic_pid_prop

__author__ = 'fyabc'


class BeginOfGame(Event):
    def __init__(self, game):
        super().__init__(game, game)

    def _repr(self):
        return super()._repr(first_player=self.game.current_player)


class BeginOfTurn(Event):
    def __init__(self, game):
        super().__init__(game, game)

    def _repr(self):
        return super()._repr(n=self.game.n_turns, player=self.game.current_player)


class EndOfTurn(Event):
    def __init__(self, game):
        super().__init__(game, game)

    def _repr(self):
        return super()._repr(n=self.game.n_turns, player=self.game.current_player)


class DrawCard(Event):
    def __init__(self, game, owner, player_id=None):
        """The event of draw a card.

        :param game:
        :param owner:
        :param player_id: The player to draw the card. If None, will be the current player when the event HAPPEN.
        """

        super().__init__(game, owner)
        self._player_id = player_id
        self.card = None

    player_id = dynamic_pid_prop()

    def _repr(self):
        return super()._repr(P=self.player_id, card=self.card)


def game_begin_standard_events(game):
    return [BeginOfGame(game), BeginOfTurn(game), DrawCard(game, None)]
