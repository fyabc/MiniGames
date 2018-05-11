#! /usr/bin/python
# -*- coding: utf-8 -*-

from .event import Event, Phase
from ...utils.game import Type

__author__ = 'fyabc'


class DeathPhase(Phase):
    """The death phase, contains some death events."""
    def __init__(self, game, death_events):
        super().__init__(game, None)
        self.deaths = death_events

    def _repr(self):
        return super()._repr(deaths=self.deaths)


class HeroDeath(Event):
    def _repr(self):
        return super()._repr(hero=self.owner)


class MinionDeath(Event):
    """The event of minion death."""
    def __init__(self, game, death, location):
        super().__init__(game, death)
        self.location = location

    def _repr(self):
        return super()._repr(minion=self.owner, loc=self.location)


class WeaponDeath(Event):
    def _repr(self):
        return super()._repr(weapon=self.owner)


def create_death_event(game, death, location=None):
    type_ = death.type

    if type_ == Type.Hero:
        return HeroDeath(game, death)
    elif type_ == Type.Minion:
        return MinionDeath(game, death, location)
    elif type_ == Type.Weapon:
        return WeaponDeath(game, death)
    else:
        raise ValueError('Unknown death type {}'.format(type_))
