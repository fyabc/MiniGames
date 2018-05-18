#! /usr/bin/python
# -*- coding: utf-8 -*-

"""Frontend utils."""

from .game import Type, Zone

__author__ = 'fyabc'


def validate_target(card, target, msg_fn):
    """Validate the target of the card.

    :param card:
    :param target:
    :param msg_fn:
    :return: The target is valid or not.
    :rtype: bool
    """

    if target is not None and card.player_id != target.player_id and target.stealth:
        msg_fn('Character with stealth cannot be targeted!')
        return False

    if not card.check_target(target):
        msg_fn('This is not a valid target!')
        return False
    return True


def validate_defender(game, zone, player_id, attacker, defender, msg_fn):
    """Validate the defender."""

    # TODO: Check zone from ``zone`` or ``defender.zone``?

    if player_id == game.current_player:
        msg_fn('Must select an enemy!')
        return False
    if zone not in (Zone.Play, Zone.Hero):
        msg_fn('This is not a valid target!')
        return False

    if defender.stealth:
        msg_fn('Character with stealth cannot be attacked!')
        return False

    if zone == Zone.Hero and not attacker.can_attack_hero:
        msg_fn('Cannot attack hero!')
        return False

    if not defender.taunt:
        defender_player = defender.game.players[defender.player_id]
        if any(e.taunt for e in defender_player.play + [defender_player.hero]):
            msg_fn('I must attack the target with taunt!')
            return False

    return True


__all__ = [
    'validate_target',
    'validate_defender',
]
