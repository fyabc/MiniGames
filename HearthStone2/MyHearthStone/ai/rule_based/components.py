#! /usr/bin/python
# -*- coding: utf-8 -*-

"""Components of rule-based AI agents."""

from ...game import player_action as pa
from ...game import player_operation as po
from ...utils.game import Type

__author__ = 'fyabc'


SelectOps = {po.PlayerOps.SelectChoice, po.PlayerOps.SelectTarget}


def have_selection(po_tree: po.PlayerOpTree):
    """Check if the PlayerOperationTree has selection."""
    tree = po_tree
    result = tree.op in SelectOps

    while not result:
        if not tree.single_child:
            return False
        tree = tree.next_op()
        if tree is None:
            return result
        else:
            result = tree.op in SelectOps

    return result


def make_pa_no_target(self, card):
    """Make the player action (without target) with given card."""
    type_ = card.type
    if type_ == Type.Minion:
        return pa.PlayMinion(self.game, card, len(self.play), None)
    elif type_ == Type.Spell:
        return pa.PlaySpell(self.game, card, None)
    elif type_ == Type.Weapon:
        return pa.PlayWeapon(self.game, card, None)
    else:
        # If the card type is unknown, just end the turn.
        return pa.TurnEnd(self.game)


def get_cost_ge_5(agent):
    return [i for i, c in enumerate(agent.hand) if c.cost >= 5]


__all__ = [
    'have_selection',
    'make_pa_no_target',
    'get_cost_ge_5',
]
