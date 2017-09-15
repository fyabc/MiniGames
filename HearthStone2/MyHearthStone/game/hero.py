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
        'CAH': [0, 1, 1],
        'description': '',
    }

    def __init__(self, game, player_id):
        super().__init__(game)
        self.player_id = player_id

    def __repr__(self):
        return super()._repr(klass_=self.data['klass'], P=self.player_id)
