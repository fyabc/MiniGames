#! /usr/bin/python
# -*- coding: utf-8 -*-

"""Summon events and related functions."""

from .event import Event

__author__ = 'fyabc'


def summon_post_process(minion):
    """Post process of summoned minion (Include transform effects and mind control effects)."""
    minion.init_attack_status()


class Summon(Event):
    def __init__(self, game, minion, loc, player_id=None):
        super().__init__(game, minion)
        self.loc = loc
        self.player_id = player_id

    @property
    def minion(self):
        return self.owner

    def _repr(self):
        return super()._repr(P=self.player_id, minion=self.owner, loc=self.loc)

    def do(self):
        summon_post_process(self.minion)
        return []


__all__ = [
    'summon_post_process',
    'Summon',
]
