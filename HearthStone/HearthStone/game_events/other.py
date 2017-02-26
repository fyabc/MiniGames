#! /usr/bin/python
# -*- coding: utf-8 -*-

from .base import GameEvent

__author__ = 'fyabc'


class FreezeEntity(GameEvent):
    """Freeze a minion or a hero."""
    pass

__all__ = [
    'FreezeEntity',
]
