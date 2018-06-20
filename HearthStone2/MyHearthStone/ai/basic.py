#! /usr/bin/python
# -*- coding: utf-8 -*-

from .agent import Agent, register_agent

from ..game import player_action as pa
from ..utils.game import Type

__author__ = 'fyabc'


@register_agent
class DefaultAgent(Agent):
    def get_player_action(self):
        return pa.TurnEnd(self.game)

    def get_replace_card(self):
        return []


@register_agent
class PlayNoTarget(Agent):
    def get_player_action(self):
        for card in self.hand:
            if not card.have_target and card.can_do_action():
                return self._make_pa(card)
        # If no available card, just end the turn.
        return pa.TurnEnd(self.game)

    def get_replace_card(self):
        return []

    def _make_pa(self, card):
        type_ = card.type
        if type_ == Type.Minion:
            return pa.PlayMinion(self.game, card, 0, None)
        elif type_ == Type.Spell:
            return pa.PlaySpell(self.game, card, None)
        elif type_ == Type.Weapon:
            return pa.PlayWeapon(self.game, card, None)
        else:
            # If the card type is unknown, just end the turn.
            return pa.TurnEnd(self.game)


__all__ = [
    'DefaultAgent',
    'PlayNoTarget',
]
