#! /usr/bin/python
# -*- coding: utf-8 -*-

from ..utils.game import Zone

__author__ = 'fyabc'


class Agent:
    AgentClasses = {}

    def __init__(self, game, player_id):
        self.game = game
        self.player_id = player_id

    @property
    def is_active(self):
        return self.game.current_player == self.player_id

    @property
    def player(self):
        return self.game.get_player(self.player_id)

    @property
    def hand(self):
        return self.game.get_zone(Zone.Hand, self.player_id)

    def get_player_action(self):
        raise NotImplementedError()

    def get_replace_card(self):
        raise NotImplementedError()


def register_agent(cls):
    if not issubclass(cls, Agent):
        raise ValueError('{} is not a subclass of Agent'.format(cls))
    Agent.AgentClasses[cls.__name__] = cls
    return cls


__all__ = [
    'Agent',
    'register_agent',
]
