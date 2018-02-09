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
        player = self.game.players[event.player_id]

        # Tire damage
        if not player.deck:
            debug('Deck empty, take tire damage!')
            event.disable()
            player.tire_counter += 1
            return standard.damage_events(self.game, self.owner, player.hero, player.tire_counter)

        card, success, new_events = self.game.move(event.player_id, Zone.Deck, 0, event.player_id, Zone.Hand, 'last')

        if success:
            event.card = card
        else:
            event.disable()

        return new_events


def add_standard_triggers(game):
    for trigger_type in [
        StdGameBegin, StdTurnBegin, StdTurnEnd, StdDrawCard,
        StdOnPlaySpell, StdSpellBlenderPhase, StdSpellText, StdAfterSpell,
        StdOnPlayMinion, StdOnBattlecry, StdAfterPlayMinion, StdAfterSummon,
        StdPreDamage, StdDamage,
        StdDeathPhase, StdHeroDeath, StdMinionDeath, StdWeaponDeath,
    ]:
        game.register_trigger(trigger_type(game))
