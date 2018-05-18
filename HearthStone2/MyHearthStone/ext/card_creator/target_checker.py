#! /usr/bin/python
# -*- coding: utf-8 -*-

"""Commonly used target checkers and testers."""

from ...utils.game import Zone, Race

__author__ = 'fyabc'


def checker_minion(self, target):
    if not super(type(self), self).check_target(target):
        return False
    if target.zone != Zone.Play:
        return False
    return True


def checker_friendly_character(self, target):
    if not super(type(self), self).check_target(target):
        return False
    if target.player_id != self.player_id:
        return False
    return True


def checker_friendly_minion(self, target):
    if not super(type(self), self).check_target(target):
        return False
    if target.zone != Zone.Play:
        return False
    if target.player_id != self.player_id:
        return False
    return True


def checker_enemy_character(self, target):
    if not super(type(self), self).check_target(target):
        return False
    if target.player_id == self.player_id:
        return False
    return True


def checker_enemy_minion(self, target):
    if not super(type(self), self).check_target(target):
        return False
    if target.zone != Zone.Play:
        return False
    if target.player_id == self.player_id:
        return False
    return True


# Have target checkers.

def have_friendly_minion(self):
    return bool(self.game.get_zone(Zone.Play, self.player_id))


def make_have_friendly_race(race):
    def _have_friendly_race(self):
        return any(race in e.race for e in self.game.get_zone(Zone.Play, self.player_id))
    return _have_friendly_race


have_friendly_beast = make_have_friendly_race(Race.Beast)


__all__ = [
    'checker_minion',
    'checker_friendly_character',
    'checker_friendly_minion',
    'checker_enemy_character',
    'checker_enemy_minion',

    'have_friendly_minion',
    'have_friendly_beast',
    'make_have_friendly_race',
]
