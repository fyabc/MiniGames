#! /usr/bin/python
# -*- coding: utf-8 -*-

from ..utils.game import Type

__author__ = 'fyabc'


# noinspection PyUnresolvedReferences
class AliveMixin:
    """The mixin class of alive entities (minions and heroes)."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.data.update({
            'attack': 0,

            # Raw health before any enchantments (need it?)
            '_raw_health': self.cls_data['health'],
            'health': self.cls_data['health'],
            'max_health': self.cls_data['health'],
        })

        self.to_be_destroyed = False  # The destroy tag for instant kill enchantments.

        # Attack numbers.
        self.n_attack = None
        self.n_total_attack = 1

        # TODO: Some minions or weapons may change this attribute?
        # Or remove this attribute?
        self.can_attack_hero = True

    @property
    def attack(self):
        return self.data['attack']

    @attack.setter
    def attack(self, value):
        self.data['attack'] = value

    @property
    def health(self):
        return self.data['health']

    @health.setter
    def health(self, value):
        self.data['health'] = value

    @property
    def max_health(self):
        return self.data['max_health']

    @max_health.setter
    def max_health(self, value):
        self.data['max_health'] = value

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
        self.data['_raw_health'] -= value

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
        self.data['attack'] = self.cls_data.get('attack', 0)
        self.data['health'] = self.data['_raw_health']
        super().aura_update_attack_health()


__all__ = [
    'AliveMixin',
]
