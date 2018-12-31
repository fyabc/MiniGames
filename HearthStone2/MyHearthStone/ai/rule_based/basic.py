#! /usr/bin/python
# -*- coding: utf-8 -*-

# TODO: Remove old agents, add new random select agents.

from .components import *
from ..agent import Agent, register_agent
from ...game import player_action as pa
from ...utils.game import Type

__author__ = 'fyabc'


@register_agent
class DefaultAgent(Agent):
    """The default agent. Can only end the turn."""
    def get_player_action(self):
        return pa.TurnEnd(self.game)

    get_replace_card = get_cost_ge_5


@register_agent
class PlayNoTarget(Agent):
    """This agent will play all available cards in hand which have no target, from left to right."""
    def get_player_action(self):
        for card in self.hand:
            po_tree = card.player_operation_tree()
            if not have_selection(po_tree) and card.can_do_action():
                return make_pa_no_target(self, card)
        # If no available card, just end the turn.
        return pa.TurnEnd(self.game)

    get_replace_card = get_cost_ge_5


@register_agent
class BaseAgent(Agent):
    def get_player_action(self):
        # Play hand.
        for card in self.hand:
            po_tree = card.player_operation_tree()
            if not have_selection(po_tree) and card.can_do_action():
                return make_pa_no_target(self, card)

        # Use hero power.
        hp = self.player.hero_power
        po_tree = hp.player_operation_tree()
        if not have_selection(po_tree) and hp.can_do_action():
            return pa.UseHeroPower(self.game, None, self.player_id)

        # If no available card, just end the turn.
        return pa.TurnEnd(self.game)

    get_replace_card = get_cost_ge_5


__all__ = [
    'DefaultAgent',
    'PlayNoTarget',
    'BaseAgent',
]
