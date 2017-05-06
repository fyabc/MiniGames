#! /usr/bin/python
# -*- coding: utf-8 -*-

from .base import GameHandler
from ..game_events import GameBegin, TurnBegin, DrawCard, AddCardToHand, Damage, PlayCard
from ..utils.debug import verbose

__author__ = 'fyabc'


class CreateCoinHandler(GameHandler):
    event_types = [GameBegin]

    def _process(self, event):
        self._message(event)
        self.game.insert_event_quick(AddCardToHand, 0, self.game.opponent_player_id)

    def _message(self, event):
        verbose('Add a coin into P{}\'s hand (not implemented)!'.format(self.game.opponent_player_id))


class DamageDeathHandler(GameHandler):
    event_types = [Damage]

    pass


class TurnBeginDrawCardHandler(GameHandler):
    """The default handler of `TurnBegin`.

    It will draw a card for current player.
    """

    event_types = [TurnBegin]

    def _process(self, event):
        self.game.insert_event_quick(DrawCard)


class ComboHandler(GameHandler):
    """The handler of combo."""

    event_types = [TurnBegin, PlayCard]

    def _process(self, event):
        if isinstance(event, TurnBegin):
            for player in self.game.players:
                player.played_cards = False
        else:
            self.game.current_player.played_cards = True


__all__ = [
    'CreateCoinHandler',
    'DamageDeathHandler',
    'TurnBeginDrawCardHandler',
    'ComboHandler',
]
