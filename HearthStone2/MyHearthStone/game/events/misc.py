#! /usr/bin/python
# -*- coding: utf-8 -*-

"""Miscellaneous events."""

from .event import Event

__author__ = 'fyabc'


class LoseDivineShield(Event):
    def _repr(self):
        return super()._repr(owner=self.owner)

    def do(self):
        return []


class LoseStealth(Event):
    def _repr(self):
        return super()._repr(owner=self.owner)

    def do(self):
        return []


class LoseDurability(Event):
    def __init__(self, game, weapon, value):
        super().__init__(game, weapon)
        self.value = value

    def _repr(self):
        return super()._repr(owner=self.owner, value=self.value)

    def do(self):
        self.owner.take_damage(self.value)
        return []


__all__ = [
    'LoseDivineShield',
    'LoseStealth',
    'LoseDurability',
]
