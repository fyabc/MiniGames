#! /usr/bin/python
# -*- coding: utf-8 -*-

from .game_event import GameEvent
from ..game_exception import GameEndException
from ..utils import verbose

__author__ = 'fyabc'


class GameBegin(GameEvent):
    def _happen(self):
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
        verbose('Turn {} (P{}) begin!'.format(self.game.turn_number, self.game.current_player_id).center(120, '='))
        self.game.current_player.turn_begin()

        # [DEBUG]
        p0, p1 = self.game.players

        verbose('''\
{}
P0: HP={} Crystal={}/{}
Hand={}
Deck={}
Desk={}
P1: HP={} Crystal={}/{}
Hand={}
Deck={}
Desk={}
{}
'''.format(
            'Begin'.center(120, '-'),
            p0.health, p0.remain_crystal, p0.total_crystal,
            p0.hand, p0.deck, p0.desk,
            p1.health, p1.remain_crystal, p1.total_crystal,
            p1.hand, p1.deck, p1.desk,
            'End'.center(120, '-'),
           ))


class TurnEnd(GameEvent):
    def __init__(self, game, player_id=None):
        super(TurnEnd, self).__init__(game)
        self.player_id = player_id if player_id is not None else game.current_player_id

    def _happen(self):
        verbose('Turn {} (P{}) end!'.format(self.game.turn_number, self.game.current_player_id))

        self.game.next_turn()
        self.game.add_events(self.game.create_event(TurnBegin))
