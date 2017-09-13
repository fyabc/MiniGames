#! /usr/bin/python
# -*- coding: utf-8 -*-

from .events.basic import BeginOfTurn, EndOfTurn

__author__ = 'fyabc'


class PlayerAction:
    """"""

    def __init__(self, game):
        self.game = game

    def phases(self):
        """Extract phases from this player action."""

        raise NotImplementedError('implemented by subclasses')


class TurnEnd(PlayerAction):
    """"""

    def __init__(self, game, player_id=None):
        super().__init__(game)
        self.player_id = game.current_player if player_id is None else player_id

    def phases(self):
        return [
            EndOfTurn(self.game), 'check_win',
            BeginOfTurn(self.game), 'check_win',
            # todo: draw card phase
        ]
