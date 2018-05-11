#! /usr/bin/python
# -*- coding: utf-8 -*-

from .game_entity import make_property
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
            'to_be_destroyed': False,   # The destroy tag for instant kill enchantments.

            # Attack related attributes.
            'n_attack': None,
            'n_total_attack': 1,
            'can_attack_hero': True,
        })

    attack = make_property('attack')
    health = make_property('health')
    max_health = make_property('max_health')
    to_be_destroyed = make_property('to_be_destroyed')
    n_attack = make_property('n_attack')
    n_total_attack = make_property('n_total_attack')
    can_attack_hero = make_property('can_attack_hero')

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
