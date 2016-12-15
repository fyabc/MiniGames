#! /usr/bin/python
# -*- encoding: utf-8 -*-

from .game_event import GameEvent
from .basic_events import GameEnd
from ..utils.debug_utils import verbose

__author__ = 'fyabc'


class Death(GameEvent):
    def __init__(self, game, entity):
        super().__init__(game)
        self.entity = entity

    def __str__(self):
        return '{}({})'.format(super().__str__(), self.entity)

    def _message(self):
        verbose('{} died!'.format(self.entity))


class MinionDeath(Death):
    def __init__(self, game, minion):
        super(MinionDeath, self).__init__(game, minion)

    @property
    def minion(self):
        return self.entity

    def _happen(self):
        self._message()

        player_id = self.game.get_player_id(self.minion)
        desk = self.game.players[player_id].desk
        assert self.minion in desk, 'The minion must in the desk'

        index = desk.index(self.minion)
        desk.remove(self.minion)

        self.minion.run_death_rattle(player_id, index)


class HeroDeath(Death):
    def __init__(self, game, player):
        super(HeroDeath, self).__init__(game, player)
        self.player_id = player.player_id

    @property
    def player(self):
        return self.entity

    def _happen(self):
        self._message()

        self.game.add_event_quick(GameEnd, self.player_id)

    def __str__(self):
        return '{}(P{})'.format(super().__str__(), self.player_id)


__all__ = [
    'Death',
    'MinionDeath',
    'HeroDeath',
]
