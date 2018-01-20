#! /usr/bin/python
# -*- coding: utf-8 -*-

"""Standard triggers.

These triggers usually do the action that 'The event happens'.

These triggers usually have the smallest oop (StandardBeforeTrigger) or largest oop (StandardAfterTrigger).
"""

from .death import *
from .play import *
from .damage import *
from .trigger import StandardBeforeTrigger
from ...utils.constants import C
from ...utils.message import debug

__author__ = 'fyabc'


class StdGameBegin(StandardBeforeTrigger):
    """Standard trigger of game begin."""

    respond = [standard.BeginOfGame]

    def process(self, event):
        debug('Game Start!'.center(C.Logging.Width, '='))

        return []


class StdTurnBegin(StandardBeforeTrigger):
    """Standard trigger of turn begin."""

    respond = [standard.BeginOfTurn]

    def process(self, event: respond[0]):
        debug('Turn Begin!'.center(C.Logging.Width, '-'))
        self.game.new_turn()

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
            debug('Deck empty, take tire damage!')
            event.disable()
            self.game.tire_counters[player_id] += 1
            return standard.damage_events(self.game, self.owner, self.game.heroes[player_id],
                                          self.game.tire_counters[player_id])

        card, success, new_events = self.game.move(player_id, Zone.Deck, 0, player_id, Zone.Hand, 'last')

        if success:
            event.card = card
        else:
            event.disable()

        return new_events


def add_standard_triggers(game):
    game.register_trigger(StdGameBegin(game))
    game.register_trigger(StdTurnBegin(game))
    game.register_trigger(StdTurnEnd(game))
    game.register_trigger(StdDrawCard(game))
    game.register_trigger(StdOnPlaySpell(game))
    game.register_trigger(StdSpellBlenderPhase(game))
    game.register_trigger(StdSpellText(game))
    game.register_trigger(StdAfterSpell(game))
    game.register_trigger(StdOnPlayMinion(game))
    game.register_trigger(StdOnBattlecry(game))
    game.register_trigger(StdAfterPlayMinion(game))
    game.register_trigger(StdAfterSummon(game))
    game.register_trigger(StdPreDamage(game))
    game.register_trigger(StdDamage(game))
    game.register_trigger(StdDeathPhase(game))
