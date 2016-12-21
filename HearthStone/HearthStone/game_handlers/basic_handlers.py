#! /usr/bin/python
# -*- coding: utf-8 -*-

from .game_handler import GameHandler
from ..game_events.basic_events import GameBegin, TurnBegin
from ..game_events.card_events import DrawCard, AddCardToHand
from ..game_events.health_events import Damage
from ..game_events.play_events import PlayCard
from ..utils.debug_utils import verbose

__author__ = 'fyabc'


class CreateCoinHandler(GameHandler):
    event_types = [GameBegin]

    def _process(self, event):
        self._message(event)
        self.game.add_event_quick(AddCardToHand, 0, self.game.opponent_player_id)
        pass

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
        self.game.add_event_quick(DrawCard)


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
