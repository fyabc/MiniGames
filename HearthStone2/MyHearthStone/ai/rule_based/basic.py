#! /usr/bin/python
# -*- coding: utf-8 -*-

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
            if not card.have_target and card.can_do_action():
                return make_pa_no_target(self, card)
        # If no available card, just end the turn.
        return pa.TurnEnd(self.game)

    get_replace_card = get_cost_ge_5


@register_agent
class BaseAgent(Agent):
    def get_player_action(self):
        # Play hand.
        for card in self.hand:
            if not card.have_target and card.can_do_action():
                return make_pa_no_target(self, card)

        # Use hero power.
        hp = self.player.hero_power
        if not hp.have_target and hp.can_do_action():
            return pa.UseHeroPower(self.game, None, self.player_id)

        # If no available card, just end the turn.
        return pa.TurnEnd(self.game)

    get_replace_card = get_cost_ge_5


__all__ = [
    'DefaultAgent',
    'PlayNoTarget',
    'BaseAgent',
]
