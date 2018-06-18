#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'fyabc'


class Agent:
    def __init__(self, game, player_id):
        self.game = game
        self.player_id = player_id

    @property
    def is_active(self):
        return self.game.current_player == self.player_id

    def get_player_action(self):
        raise NotImplementedError()

    def get_replace_card(self):
        raise NotImplementedError()


__all__ = [
    'Agent',
]
