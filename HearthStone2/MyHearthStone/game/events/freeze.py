#! /usr/bin/python
# -*- coding: utf-8 -*-

"""Freeze events."""

from .event import Event

__author__ = 'fyabc'


class Freeze(Event):
    def __init__(self, game, owner, target):
        super().__init__(game, owner)
        self.target = target

    def _repr(self):
        return super()._repr(source=self.owner, target=self.target)

    def do(self):
        self.target.frozen = True
        return []


__all__ = [
    'Freeze',
]
