#! /usr/bin/python
# -*- coding: utf-8 -*-

from .game_entity import GameEntity, SetDataMeta
from ..utils.game import Zone

__author__ = 'fyabc'


class Hero(GameEntity, metaclass=SetDataMeta):
    """[NO_DESCRIPTION]"""

    _data = {
        'klass': 0,
        'CAH': [None, None, 30],
    }

    def __init__(self, game, player_id):
        super().__init__(game)

        self.zone = Zone.Invalid
        self.play_state = True  # False means lose. When this hero removed from play, set it to False.
        self.player_id = player_id
        self.health = self.data['CAH'][2]
        self.orig_health = self.data['CAH'][2]  # The original health.
        self.max_health = self.health
        self.to_be_destroyed = False  # The destroy tag for instant kill enchantments.

        self.oop = self.game.oop

    def __repr__(self):
        return super()._repr(klass=self.data['klass'], P=self.player_id)

    @property
    def alive(self):
        return self.health > 0 and not self.to_be_destroyed
