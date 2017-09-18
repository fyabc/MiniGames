#! /usr/bin/python
# -*- coding: utf-8 -*-

from .event import Event, Phase

__author__ = 'fyabc'


class PreDamage(Phase):
    def __init__(self, game, damage):
        super().__init__(game, damage.owner)
        self.damage = damage

    def message(self):
        super().message(source=self.owner, target=self.damage.target, value=self.damage.value)


class Damage(Phase):
    def __init__(self, game, owner, target, value):
        super().__init__(game, owner)
        self.target = target
        self.value = value

    def message(self):
        super().message(source=self.owner, target=self.target, value=self.value)


def damage_events(game, owner, target, value):
    """Utility to get damage event sequences."""

    damage = Damage(game, owner, target, value)
    return [
        PreDamage(game, damage),
        damage,
    ]
