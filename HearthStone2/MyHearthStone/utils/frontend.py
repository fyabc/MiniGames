#! /usr/bin/python
# -*- coding: utf-8 -*-

"""Frontend utils."""

__author__ = 'fyabc'


def validate_target(card, target, msg_fn):
    """Validate the target of the card.

    :param card:
    :param target:
    :param msg_fn:
    :return: The target is valid or not.
    :rtype: bool
    """

    # TODO: Move it into ``Card``.

    if target is not None and card.player_id != target.player_id and target.stealth:
        msg_fn('Character with stealth cannot be targeted!')
        return False

    if not card.check_target(target):
        msg_fn('This is not a valid target!')
        return False
    return True


__all__ = [
    'validate_target',
]
