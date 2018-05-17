#! /usr/bin/python
# -*- coding: utf-8 -*-

"""Commonly used target checkers."""

from ...utils.game import Zone

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


__all__ = [
    'checker_minion',
    'checker_friendly_character',
    'checker_friendly_minion',
    'checker_enemy_character',
    'checker_enemy_minion',
]
