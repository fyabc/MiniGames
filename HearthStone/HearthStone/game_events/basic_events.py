#! /usr/bin/python
# -*- coding: utf-8 -*-

from .game_event import GameEvent
from ..game_exception import GameEndException
from ..utils import verbose, Config

__author__ = 'fyabc'


windowWidth = Config['CLI']['windowWidth']


class GameBegin(GameEvent):
    def _happen(self):
        verbose('Game begin!'.center(windowWidth, Config['CLI']['charGameBegin']))
        # todo: add more actions, such as card selection
        self.game.add_event_quick(TurnBegin)


class GameEnd(GameEvent):
    def _happen(self):
        verbose('Game end!')
        raise GameEndException(self.game.current_player_id)


class TurnBegin(GameEvent):
    def __init__(self, game, player_id=None):
        super(TurnBegin, self).__init__(game)
        self.player_id = player_id if player_id is not None else game.current_player_id

    def _happen(self):
        verbose('Turn {} (P{}) begin!'
                .format(self.game.turn_number, self.game.current_player_id)
                .center(windowWidth, Config['CLI']['charTurnBegin']))
        self.game.current_player.turn_begin()


class TurnEnd(GameEvent):
    def __init__(self, game, player_id=None):
        super(TurnEnd, self).__init__(game)
        self.player_id = player_id if player_id is not None else game.current_player_id

    def _happen(self):
        verbose('Turn {} (P{}) end!'
                .format(self.game.turn_number, self.game.current_player_id)
                .center(windowWidth, Config['CLI']['charTurnEnd']))

        self.game.next_turn()
        self.game.add_events(self.game.create_event(TurnBegin))


__all__ = [
    'GameBegin',
    'GameEnd',
    'TurnBegin',
    'TurnEnd',
]
