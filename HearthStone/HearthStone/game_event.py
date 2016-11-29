#! /usr/bin/python
# -*- coding: utf-8 -*-

from HearthStone.event_framework import Event

__author__ = 'fyabc'


class GameEvent(Event):
    def __init__(self, game):
        super(GameEvent, self).__init__()
        self.game = game

    def happen(self):
        print('{} happen!'.format(self))


class TurnBegin(GameEvent):
    def __init__(self, game, player_id=None):
        super(TurnBegin, self).__init__(game)
        self.player_id = player_id if player_id is not None else game.current_player_id


class TurnEnd(GameEvent):
    def __init__(self, game, player_id=None):
        super(TurnEnd, self).__init__(game)
        self.player_id = player_id if player_id is not None else game.current_player_id


__all__ = [
    'GameEvent',
    'TurnBegin',
    'TurnEnd',
]
