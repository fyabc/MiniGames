#! /usr/bin/python
# -*- encoding: utf-8 -*-

from .game_event import GameEvent
from ..utils.debug_utils import verbose

__author__ = 'fyabc'


class MinionDeath(GameEvent):
    def __init__(self, game, minion):
        super(MinionDeath, self).__init__(game)
        self.minion = minion

    def __str__(self):
        return '{}({})'.format(super(MinionDeath, self).__str__(), self.minion)

    def _happen(self):
        self._message()

        player_id = self.game.get_player_id(self.minion)
        desk = self.game.players[player_id].desk
        assert self.minion in desk, 'The minion must in the desk'

        index = desk.index(self.minion)
        desk.remove(self.minion)

        self.minion.run_death_rattle(player_id, index)

    def _message(self):
        verbose('{} died!'.format(self.minion))


__all__ = [
    'MinionDeath',
]
