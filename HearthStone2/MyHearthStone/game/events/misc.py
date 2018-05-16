#! /usr/bin/python
# -*- coding: utf-8 -*-

"""Miscellaneous events."""

from .event import Event

__author__ = 'fyabc'


class LoseDivineShield(Event):
    def do(self):
        return []


class LoseStealth(Event):
    def do(self):
        return []


__all__ = [
    'LoseDivineShield',
    'LoseStealth',
]
