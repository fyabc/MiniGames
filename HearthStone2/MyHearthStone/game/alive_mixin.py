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

        # Data of alive entities.
        # [NOTE]: Attributes like "divine_shield" and "stealth" must NOT be set in it,
        # since it is called after initializer, it will overwrite the card specific value.
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

    attack = make_property('attack', setter=False)
    health = make_property('health', setter=False)
    max_health = make_property('max_health', setter=False)
    to_be_destroyed = make_property('to_be_destroyed')

    # Other attributes.
    divine_shield = make_property('divine_shield', default=False)
    stealth = make_property('stealth', default=False)
    taunt = make_property('taunt', default=False)

    n_attack = make_property('n_attack')
    n_total_attack = make_property('n_total_attack')
    can_attack_hero = make_property('can_attack_hero')

    @property
    def alive(self):
        return self.health > 0 and not self.to_be_destroyed

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

    def restore_health(self, value):
        """

        :param value: The proposed heal value
        :return: The real heal value
        """
        real_heal = min(value, self.data['max_health'] - self.data['health'])
        self.data['_raw_health'] += real_heal

        return real_heal

    def inc_health(self, value):
        """Increase health and max-health."""
        self.data['health'] += value
        self.data['max_health'] += value

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
        self.data['max_health'] = self.cls_data['health']
        super().aura_update_attack_health()


__all__ = [
    'AliveMixin',
]
