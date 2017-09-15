#! /usr/bin/python
# -*- coding: utf-8 -*-

"""Standard triggers.

These triggers usually do the action that 'The event happens'.

These triggers usually have the smallest oop (StandardBeforeTrigger) or largest oop (StandardAfterTrigger).
"""

from .trigger import Trigger
from ..events import standard
from ...utils.game import Zone
from ...utils.message import message
from ...utils.constants import C

__author__ = 'fyabc'


class StandardBeforeTrigger(Trigger):
    """Class of standard triggers that run before any other triggers."""

    def __init__(self, game):
        super().__init__(game, game)

    def process(self, event):
        event.message()

        return []


class StandardAfterTrigger(Trigger):
    """Class of standard triggers that run after any other triggers."""

    OopMax = 1 << 31

    def __init__(self, game):
        super().__init__(game, game)
        self._oop = self.OopMax

    @property
    def oop(self):
        return self._oop

    def process(self, event):
        event.message()

        return []


class StdGameBegin(StandardBeforeTrigger):
    """Standard trigger of game begin."""

    respond = [standard.BeginOfGame]

    def process(self, event):
        message('Game Start!'.center(C.Logging.Width, '='))
        event.message()

        return []


class StdTurnBegin(StandardBeforeTrigger):
    """Standard trigger of turn begin."""

    respond = [standard.BeginOfTurn]

    def process(self, event: respond[0]):
        message('Turn Begin!'.center(C.Logging.Width, '-'))
        self.game.new_turn()
        event.message()

        return []


class StdTurnEnd(StandardBeforeTrigger):
    """Standard trigger of turn end (may useless)."""

    respond = [standard.EndOfTurn]


class StdDrawCard(StandardBeforeTrigger):
    """Standard trigger of drawing cards."""

    respond = [standard.DrawCard]

    def process(self, event: respond[0]):
        player_id = event.player_id

        # Tire damage
        if not self.game.decks[player_id]:
            event.message()
            message('Deck empty, take tire damage!')
            event.disable()
            self.game.tire_counters[player_id] += 1
            return [standard.PreDamage(self.game, self.owner, self.game.heroes[player_id],
                                       self.game.tire_counters[player_id])]

        card, success, new_events = self.game.move(player_id, Zone.Deck, 0, player_id, Zone.Hand, 'last')

        if success:
            event.card = card
            event.message()
        else:
            event.message()
            event.disable()

        return new_events


class StdPreDamage(StandardBeforeTrigger):
    """Standard trigger of pre-damage."""

    respond = [standard.PreDamage]

    def process(self, event: respond[0]):
        event.message()

        if event.value <= 0:
            return []

        # todo

        return [standard.Damage(event.game, event.owner, event.target, event.value)]


class StdDamage(StandardBeforeTrigger):
    """Standard trigger of damage."""

    respond = [standard.Damage]

    def process(self, event: respond[0]):
        event.message()

        return []


def add_standard_triggers(game):
    game.register_trigger(StdGameBegin(game))
    game.register_trigger(StdTurnBegin(game))
    game.register_trigger(StdTurnEnd(game))
    game.register_trigger(StdDrawCard(game))
    game.register_trigger(StdPreDamage(game))
    game.register_trigger(StdDamage(game))
