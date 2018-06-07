#! /usr/bin/python
# -*- coding: utf-8 -*-

"""This module include all standard events."""

from .event import Event
from .play import *
from .damage import *
from .healing import *
from .card_moving import *
from .summon import *
from .death import *
from .combat import *
from .hero_power import *
from .freeze import *
from .misc import *
from .utils import dynamic_pid_prop
from ...utils.constants import C
from ...utils.game import Zone
from ...utils.message import debug

__author__ = 'fyabc'


class BeginOfGame(Event):
    def __init__(self, game):
        super().__init__(game, game)

    def _repr(self):
        return super()._repr(first_player=self.game.current_player)

    def do(self):
        debug('Game Start!'.center(C.Logging.Width, '='))
        return []


class BeginOfTurn(Event):
    def __init__(self, game):
        super().__init__(game, game)

    @property
    def player_id(self):
        # [NOTE]: After this event happens, the current player id has been changed.
        return self.game.current_player

    def _repr(self):
        return super()._repr(n=self.game.n_turns, player=self.game.current_player)

    def do(self):
        debug('Turn Begin!'.center(C.Logging.Width, '-'))
        self.game.new_turn()

        return []


class EndOfTurn(Event):
    def __init__(self, game):
        super().__init__(game, game)

    @property
    def player_id(self):
        # [NOTE]: Before and after this event happens, the current player id has not been changed.
        return self.game.current_player

    def _repr(self):
        return super()._repr(n=self.game.n_turns, player=self.player_id)

    def do(self):
        return []


def game_begin_standard_events(game):
    return [BeginOfGame(game), BeginOfTurn(game), DrawCard(game, None)]
