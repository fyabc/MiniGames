#! /usr/bin/python
# -*- coding: utf-8 -*-

from .game_entity import GameEntity
from .alive_mixin import AliveMixin
from ..utils.game import Zone, Type

__author__ = 'fyabc'


class Hero(AliveMixin, GameEntity):
    """The class of hero."""

    data = {
        'type': Type.Hero,
        'klass': 0,
        'health': 30,
    }

    def __init__(self, game, player_id):
        super().__init__(game)

        self.data.update({
            'player_id': player_id,
        })

        # todo: How to assign weapon attributes to hero attributes?

        self.play_state = True  # False means lose. When this hero removed from play, set it to False.

        self.oop = self.game.entity.oop

    def __repr__(self):
        return super()._repr(klass=self.data['klass'], P=self.player_id, health=self.health)

    def run_deathrattle(self):
        """Run the deathrattle. Implemented in subclasses.

        :return: list of events.
        """
        return []


class HeroPower(GameEntity):
    """The class of hero power."""

    _data = {
        'type': Type.HeroPower,
        'cost': 2,
        'have_target': False,
    }

    def __init__(self, game, player_id):
        super().__init__(game)

        self.data.update({
            'cost': self.cls_data['cost'],
            'player_id': player_id,
        })

    @property
    def cost(self):
        return max(self.data['cost'], 0)

    @property
    def have_target(self):
        return self.data['have_target']

    def check_target(self, target):
        if not self.have_target:
            return True

        # Default valid target zones.
        #   Only support target to `Play` and `Hero` zones now.
        #   Can support `Hand`, `Weapon` and other zones in future.
        # [NOTE]: Only cards, heroes and hero powers have attribute zone.
        zone = target.zone
        if zone not in (Zone.Play, Zone.Hero):
            return False

        return True

    def run(self, target):
        return []
