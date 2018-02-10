#! /usr/bin/python
# -*- coding: utf-8 -*-

from .game_entity import GameEntity
from ..utils.game import Zone

__author__ = 'fyabc'


class Hero(GameEntity):
    """The class of hero."""

    data = {
        'klass': 0,
        'health': 30,
    }

    def __init__(self, game, player_id):
        super().__init__(game)

        self.zone = Zone.Invalid
        self.play_state = True  # False means lose. When this hero removed from play, set it to False.
        self.player_id = player_id
        self.attack = 0
        self._raw_health = self.data['health']
        self.health = self.data['health']
        self.max_health = self.health
        self.to_be_destroyed = False  # The destroy tag for instant kill enchantments.

        self.oop = self.game.oop

    def __repr__(self):
        return super()._repr(klass=self.data['klass'], P=self.player_id)

    @property
    def alive(self):
        return self.health > 0 and not self.to_be_destroyed

    def run_deathrattle(self):
        """Run the deathrattle. Implemented in subclasses.

        :return: list of events.
        """
        return []

    def take_damage(self, value):
        self._raw_health -= value

    def aura_update_attack_health(self):
        self.health = self._raw_health
        super().aura_update_attack_health()


class HeroPower(GameEntity):
    """The class of hero power."""

    _data = {
        'cost': 2,
        'have_target': False,
    }

    def __init__(self, game, player_id):
        super().__init__(game)

        self.zone = Zone.Invalid
        self.player_id = player_id
        self._cost = self.data['cost']

    @property
    def cost(self):
        return max(self._cost, 0)

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
