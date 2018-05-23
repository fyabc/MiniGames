#! /usr/bin/python
# -*- coding: utf-8 -*-

"""Commonly used frontend checkers.

Contains:
    Action checker      (used as ``can_do_action`` method)
    Target tester       (used as ``have_target`` method)
    Target checker      (used as ``check_target`` method)
    Entity collector    (used to collect target entities in battlecry/deathrattle/run methods)
"""

from ...utils.game import Zone, Race

__author__ = 'fyabc'


# Action checkers.

def require_board_not_full(self, msg_fn=None):
    """The ``can_do_action`` method that require the board not full.

    Used by many spells that will summon a minion.
    """
    super_result = super(type(self), self).can_do_action(msg_fn=msg_fn)
    if super_result == self.Inactive:
        return super_result

    if self.game.full(Zone.Play, self.player_id):
        if msg_fn:
            msg_fn('I have too many minions, and I can\'t use it!')
        return self.Inactive

    return super_result


# Target testers.

def have_friendly_minion(self):
    return bool(self.game.get_zone(Zone.Play, self.player_id))


def make_have_friendly_race(race):
    def _have_friendly_race(self):
        return any(race in e.race for e in self.game.get_zone(Zone.Play, self.player_id))
    return _have_friendly_race


have_friendly_beast = make_have_friendly_race(Race.Beast)


# Target checkers.

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


def checker_my_hand(self, target):
    """The target checker of my hand.

    This checker is used for DIY cards that will select your hand as target.
    Example: Battlecry: Select and discard a card from you hand.
    """
    if target is None:
        return True

    zone, player_id = target.zone, target.player_id
    if zone == Zone.Hand and player_id == self.player_id and target != self:
        return True
    return False


# Entity collectors.


__all__ = [
    'require_board_not_full',

    'have_friendly_minion',
    'have_friendly_beast',
    'make_have_friendly_race',

    'checker_minion',
    'checker_friendly_character',
    'checker_friendly_minion',
    'checker_enemy_character',
    'checker_enemy_minion',
    'checker_my_hand',
]
