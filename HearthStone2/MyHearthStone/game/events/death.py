#! /usr/bin/python
# -*- coding: utf-8 -*-

from .event import Event, Phase

__author__ = 'fyabc'


class DeathPhase(Phase):
    def __init__(self, game, deaths):
        super().__init__(game, None)
        self.deaths = deaths

    def _repr(self):
        return super()._repr(deaths=self.deaths)


class HeroDeath(Event):
    def _repr(self):
        return super()._repr(hero=self.owner)


class MinionDeath(Event):
    def _repr(self):
        return super()._repr(minion=self.owner)


class WeaponDeath(Event):
    def _repr(self):
        return super()._repr(weapon=self.owner)
