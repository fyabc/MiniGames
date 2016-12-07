#! /usr/bin/python
# -*- coding: utf-8 -*-

from .game_handler import GameHandler
from ..game_events import GameBegin, CreateCardToHand, Damage
from ..utils.debug_utils import verbose

__author__ = 'fyabc'


class CreateCoinHandler(GameHandler):
    event_types = [GameBegin]

    def _process(self, event):
        self._message(event)
        # self.game.add_event_quick(CreateCardToHand, None, self.game.opponent_player_id)
        pass

    def _message(self, event):
        verbose('Add a coin into P{}\'s hand (not implemented)!'.format(self.game.opponent_player_id))


class DamageDeathHandler(GameHandler):
    event_types = [Damage]

    pass


__all__ = [
    'CreateCoinHandler',
]