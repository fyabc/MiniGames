#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'fyabc'


class AliveMixin:
    """The mixin class of alive entities (minions and heroes)."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # todo: Change these attributes (attack, health, etc) to read-only properties.

        self.attack = 0
        self._raw_health = self.data['health']
        self.health = self.data['health']
        self.max_health = self.health

        self.to_be_destroyed = False  # The destroy tag for instant kill enchantments.

        # Attack numbers.
        self.n_attack = 0
        self.n_total_attack = 1

    @property
    def alive(self):
        return self.health > 0 and not self.to_be_destroyed

    @property
    def taunt(self):
        return False

    @property
    def exhausted(self):
        return self.n_attack >= self.n_total_attack

    def take_damage(self, value):
        self._raw_health -= value

    def inc_n_attack(self):
        self.n_attack += 1

    def set_exhausted(self):
        self.n_attack = self.n_total_attack

    def clear_exhausted(self):
        self.n_attack = 0


__all__ = [
    'AliveMixin',
]
