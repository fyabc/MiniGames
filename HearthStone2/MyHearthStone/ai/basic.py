#! /usr/bin/python
# -*- coding: utf-8 -*-

from .agent import Agent

from ..game import player_action as pa

__author__ = 'fyabc'


class DefaultAgent(Agent):
    def get_player_action(self):
        return pa.TurnEnd(self.game)

    def get_replace_card(self):
        return []


__all__ = [
    'DefaultAgent',
]
