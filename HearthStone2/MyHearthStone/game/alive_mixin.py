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

        # Temporary data dict for aura update.
        self.aura_tmp = {}

    def _reset_tags(self):
        # Data of alive entities.
        self.data.update({
            'attack': 0,
            'damage': 0,
            'max_health': self.cls_data['health'],
            'to_be_destroyed': False,  # The destroy tag for instant kill enchantments.

            # Attack related attributes.
            'n_attack': None,
            'n_total_attack': 1,
            'can_attack_hero': True,
        })

    # Health-related properties.

    damage = make_property('damage')
    to_be_destroyed = make_property('to_be_destroyed')

    @property
    def alive(self):
        return self.data['damage'] < self.data['max_health'] and not self.to_be_destroyed

    def _get_max_health(self):
        return self.data['max_health']

    def _set_max_health(self, value):
        # If max health is reduced, reduce damage value.
        orig_max_h = self.data['max_health']
        if orig_max_h > value:
            self.data['damage'] = max(0, self.data['damage'] - (orig_max_h - value))
        self.data['max_health'] = value

    max_health = property(_get_max_health, _set_max_health)

    @property
    def health(self):
        return self.data['max_health'] - self.data['damage']

    @property
    def damaged(self):
        return self.data['damage'] > 0

    def take_damage(self, value):
        self.data['damage'] += value

    def restore_health(self, value):
        """

        :param value: The proposed heal value
        :return: The real heal value
        """
        real_heal = min(value, self.data['damage'])
        self.data['damage'] -= real_heal

        return real_heal

    # Attack-related properties.

    attack = make_property('attack')
    n_attack = make_property('n_attack')
    n_total_attack = make_property('n_total_attack')
    can_attack_hero = make_property('can_attack_hero')

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

    # Other attributes.
    divine_shield = make_property('divine_shield', default=False)
    stealth = make_property('stealth', default=False)
    taunt = make_property('taunt', default=False)

    # Aura related.

    def aura_update_attack_health(self):
        self.aura_tmp.update({
            'attack': self.cls_data.get('attack', 0),
            'max_health': self.cls_data['health'],
        })
        super().aura_update_attack_health()

        # Set new value after aura update, something will be do automatically here (such as value change of max_health)
        self.attack = self.aura_tmp['attack']
        self.max_health = self.aura_tmp['max_health']


__all__ = [
    'AliveMixin',
]
