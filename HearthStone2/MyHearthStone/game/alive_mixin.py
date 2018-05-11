#! /usr/bin/python
# -*- coding: utf-8 -*-

from ..utils.game import Type

__author__ = 'fyabc'


class AliveMixin:
    """The mixin class of alive entities (minions and heroes)."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # todo: Change these attributes (attack, health, etc) to values in data.

        self.attack = 0
        self._raw_health = self.data['health']
        self.health = self.data['health']
        self.max_health = self.health

        self.to_be_destroyed = False  # The destroy tag for instant kill enchantments.

        # Attack numbers.
        self.n_attack = None
        self.n_total_attack = 1

        # TODO: Some minions or weapons may change this attribute?
        # Or remove this attribute?
        self.can_attack_hero = True

    @property
    def alive(self):
        return self.health > 0 and not self.to_be_destroyed

    @property
    def taunt(self):
        return False

    @property
    def exhausted(self):
        return self.n_attack >= self.n_total_attack

    @property
    def attack_status(self):
        if self.n_attack is None:
            return 'sleep'
        if self.n_attack >= self.n_total_attack:
            return 'exhausted'
        return 'ready'

    def take_damage(self, value):
        self._raw_health -= value

    def inc_n_attack(self):
        self.n_attack += 1

    def init_attack_status(self):
        """Initialize attack state when the object."""

        if self.type == Type.Hero:
            self.n_attack = 0
            return

        # This is a minion
        if self.charge:
            self.n_attack = 0
            return

        if self.rush:
            self.n_attack = 0
            self.can_attack_hero = False
        self.n_attack = None

    def reset_attack_status(self):
        self.n_attack = 0
        self.can_attack_hero = True

    def aura_update_attack_health(self):
        self.attack = self.data.get('attack', 0)
        self.health = self._raw_health
        super().aura_update_attack_health()


__all__ = [
    'AliveMixin',
]
