#! /usr/bin/python
# -*- coding: utf-8 -*-

from .game_entity import GameEntity, SetDataMeta

__author__ = 'fyabc'


class Hero(GameEntity, metaclass=SetDataMeta):
    """[NO_DESCRIPTION]"""

    _data = {
        'id': None,
        'name': '',
        'package': 0,
        'klass': 0,
        'CAH': [None, None, 30],
        'description': '',
    }

    def __init__(self, game, player_id):
        super().__init__(game)

        self.player_id = player_id
        self.health = self.data['CAH'][2]
        self.max_health = self.health
        self.to_be_destroyed = False  # The destroy tag for instant kill enchantments.

        self.oop = self.game.oop

    def __repr__(self):
        return super()._repr(klass=self.data['klass'], P=self.player_id)
