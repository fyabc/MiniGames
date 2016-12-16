#! /usr/bin/python
# -*- coding: utf-8 -*-

from .game_event import GameEvent
from ..utils import verbose, Config

__author__ = 'fyabc'


windowWidth = Config['CLI']['windowWidth']


class GameBegin(GameEvent):
    def _happen(self):
        self._message()

        # todo: add more actions, such as card selection
        self.game.add_event_quick(TurnBegin)

    def _message(self):
        verbose('Game begin!'.center(windowWidth, Config['CLI']['charGameBegin']))


class GameEnd(GameEvent):
    def __init__(self, game, loser_id=None):
        super(GameEnd, self).__init__(game)
        self.current_player_id = self.game.current_player_id
        self.loser_id = loser_id or self.game.current_player_id

    def _happen(self):
        self._message()

        # raise GameEndException(self.game.current_player_id)

    def _message(self):
        verbose('Game end! Current player: P{}, loser: P{}'.format(self.current_player_id, self.loser_id))


class TurnBegin(GameEvent):
    def __init__(self, game, player_id=None):
        super(TurnBegin, self).__init__(game)
        self.player_id = player_id if player_id is not None else game.current_player_id

    def _happen(self):
        self._message()

        self.game.current_player.turn_begin()

    def _message(self):
        verbose('Turn {} (P{}) begin!'
                .format(self.game.turn_number, self.game.current_player_id)
                .center(windowWidth, Config['CLI']['charTurnBegin']))


class TurnEnd(GameEvent):
    def __init__(self, game, player_id=None):
        super(TurnEnd, self).__init__(game)
        self.player_id = player_id if player_id is not None else game.current_player_id

    def _happen(self):
        self._message()

        self.game.current_player.turn_end()
        self.game.next_turn()
        self.game.add_event_quick(TurnBegin)

    def _message(self):
        verbose('Turn {} (P{}) end!'
                .format(self.game.turn_number, self.game.current_player_id)
                .center(windowWidth, Config['CLI']['charTurnEnd']))


__all__ = [
    'GameBegin',
    'GameEnd',
    'TurnBegin',
    'TurnEnd',
]
