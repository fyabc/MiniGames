#! /usr/bin/python
# -*- encoding: utf-8 -*-

from .game_event import GameEvent
from .damage_events import Damage

__author__ = 'fyabc'


class Attack(GameEvent):
    pass


__all__ = [
    'Attack',
]
