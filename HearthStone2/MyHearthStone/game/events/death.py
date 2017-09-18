#! /usr/bin/python
# -*- coding: utf-8 -*-

from .event import Event, Phase

__author__ = 'fyabc'


class DeathPhase(Phase):
    def __init__(self, game, deaths):
        super().__init__(game, None)
        self.deaths = deaths

    def message(self):
        super().message(deaths=self.deaths)


class HeroDeath(Event):
    def message(self):
        super().message(hero=self.owner)


class MinionDeath(Event):
    def message(self):
        super().message(minion=self.owner)


class WeaponDeath(Event):
    def message(self):
        super().message(weapon=self.owner)
