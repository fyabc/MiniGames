#! /usr/bin/python
# -*- coding: utf-8 -*-

from .game_handler import GameHandler
from ..game_events.damage_events import Damage
from ..utils.debug_utils import verbose

__author__ = 'fyabc'


class FreezeOnDamage(GameHandler):
    """The handler of '冻结所有受到该随从伤害的随从'."""

    event_types = [Damage]

    def __init__(self, game, owner):
        super(FreezeOnDamage, self).__init__(game, owner)

    def _process(self, event):
        if self.owner != event.source:
            return
        event.target.freeze()
        self._message(event)

    def _message(self, event):
        verbose('{} freeze {}!'.format(self.owner, event.target))


__all__ = [
    'FreezeOnDamage',
]
