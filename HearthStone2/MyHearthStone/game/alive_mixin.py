#! /usr/bin/python
# -*- coding: utf-8 -*-

from .game_entity import make_property
from ..utils.game import Type, Zone

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
            'armor': 0,                 # [NOTE]: Even support armor for minions (for future DIYs).
            'to_be_destroyed': False,   # The destroy tag for instant kill enchantments.

            # Attack related attributes.
            'n_attack': None,
            'n_total_attack': 1,
            'can_attack_hero': True,
        })

    # Health-related properties.

    damage = make_property('damage')
    armor = make_property('armor')
    to_be_destroyed = make_property('to_be_destroyed')

    @property
    def alive(self):
        return self.data['damage'] < self.data['max_health'] + self.data['armor'] and not self.to_be_destroyed

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
        if value <= self.data['armor']:
            self.data['armor'] -= value
            return
        value -= self.data['armor']
        self.data['armor'] = 0
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

    n_attack = make_property('n_attack')
    n_total_attack = make_property('n_total_attack')
    can_attack_hero = make_property('can_attack_hero')

    @property
    def attack(self):
        return max(0, self.data['attack'])

    @attack.setter
    def attack(self, value):
        self.data['attack'] = value

    @property
    def exhausted(self):
        return self.n_attack >= self.n_total_attack

    @property
    def attack_status(self):
        if self.n_attack is None:
            return 'sleep'
        if self.n_attack >= self.n_total_attack:
            return 'exhausted'
        # TODO: Add other status, such as 'cannot attack'?
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
    immune = make_property('immune', default=False)

    @property
    def taunt(self):
        return self.data.get('taunt', False) and not self.stealth and not self.immune

    @taunt.setter
    def taunt(self, value):
        self.data['taunt'] = value

    @property
    def negated_taunt(self):
        return self.taunt and (self.stealth or self.immune)

    # Aura related.

    def can_do_action(self, msg_fn=None):
        super_result = super().can_do_action(msg_fn=msg_fn)
        if super_result == self.Inactive:
            return super_result

        # Entities with alive mixin can only be in ``Zone.Play`` or ``Zone.Hero``.
        if self.zone not in (Zone.Play, Zone.Hero):
            return super_result

        type_ = self.type
        # If in play, test if can attack.
        attack_status = self.attack_status
        if attack_status == 'sleep':
            if msg_fn:
                if type_ == Type.Hero:
                    msg_fn('I am not ready!')
                else:
                    msg_fn('This minion is not ready!')
            return self.Inactive
        else:
            if self.attack <= 0:
                if msg_fn:
                    if type_ == Type.Hero:
                        msg_fn('I cannot attack!')
                    else:
                        msg_fn('This minion cannot attack!')
                return self.Inactive
            else:
                if attack_status == 'exhausted':
                    if msg_fn:
                        if type_ == Type.Hero:
                            msg_fn('I have attacked!')
                        else:
                            msg_fn('This minion has attacked!')
                    return self.Inactive
                else:
                    assert attack_status == 'ready'
        return super_result


__all__ = [
    'AliveMixin',
]
