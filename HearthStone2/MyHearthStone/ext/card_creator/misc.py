#! /usr/bin/python
# -*- coding: utf-8 -*-

"""Miscellaneous helper functions."""

from ...utils.game import Zone

__author__ = 'fyabc'


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


__all__ = [
    'require_board_not_full',
]
