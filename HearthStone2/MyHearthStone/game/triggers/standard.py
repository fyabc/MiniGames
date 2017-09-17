#! /usr/bin/python
# -*- coding: utf-8 -*-

"""Standard triggers.

These triggers usually do the action that 'The event happens'.

These triggers usually have the smallest oop (StandardBeforeTrigger) or largest oop (StandardAfterTrigger).
"""

from .trigger import Trigger
from ..events import standard
from ..card import Minion, Weapon
from ..hero import Hero
from ...utils.game import Zone, error_and_stop
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
            return standard.damage_events(self.game, self.owner, self.game.heroes[player_id],
                                          self.game.tire_counters[player_id])

        card, success, new_events = self.game.move(player_id, Zone.Deck, 0, player_id, Zone.Hand, 'last')

        if success:
            event.card = card
            event.message()
        else:
            event.message()
            event.disable()

        return new_events


class StdOnPlaySpell(StandardBeforeTrigger):
    """Standard trigger of OnPlaySpell."""

    respond = [standard.OnPlaySpell]

    def process(self, event: respond[0]):
        """Process the OnPlaySpell event.

        The card is removed from your hand and enters Play and its Mana cost is paid.
        If it targets, the target is remembered (and its validity is not checked again).
        (If Bloodbloom or Cho'Gall is out, you take damage instead.
        This damage is resolved immediately, e.g. for Floating Watcher.)

        :param event: The event to be processed.
        :return: new event list.
        """

        player_id = event.player_id

        # todo: Add effect of Cho'gall
        if self.game.mana[player_id] < event.spell.cost:
            error_and_stop(self.game, event, 'You do not have enough mana!')
            return []

        if not event.spell.check_target(event.target):
            error_and_stop(self.game, event, 'This is not a valid target!')
            return []

        if event.spell.data['secret']:
            if self.game.full(Zone.Secret, player_id):
                error_and_stop(self.game, event, 'I cannot have more secrets!')
                return []

            for card in self.game.get_zone(Zone.Secret, player_id):
                if card.data['id'] == event.spell.data['id']:
                    error_and_stop(self.game, event, 'I already have this secret!')
                    return []

        event.message()

        tz = Zone.Graveyard
        if event.spell.data['secret']:
            tz = Zone.Secret

        self.game.move(player_id, Zone.Hand, event.spell, player_id, tz, 'last')

        return []


class StdSpellBlenderPhase(StandardBeforeTrigger):
    """Standard trigger of SpellBlenderPhase (may be useless?)."""

    respond = [standard.SpellBenderPhase]

    def process(self, event: respond[0]):
        event.message()
        return []


class StdSpellText(StandardBeforeTrigger):
    """Standard trigger of SpellText."""

    respond = [standard.SpellText]

    def process(self, event: respond[0]):
        event.message()
        return event.spell.run(event.target)


class StdAfterSpell(StandardBeforeTrigger):
    """Standard trigger of AfterSpell (may be useless?)."""

    respond = [standard.AfterSpell]

    def process(self, event: respond[0]):
        event.message()
        return []


class StdPreDamage(StandardBeforeTrigger):
    """Standard trigger of pre-damage."""

    respond = [standard.PreDamage]

    def process(self, event: respond[0]):
        event.message()

        if event.damage.value <= 0:
            # [NOTE] May need to remain this event here?
            event.disable()
            self.game.stop_subsequent_phases()
            return []

        # todo

        return []


class StdDamage(StandardBeforeTrigger):
    """Standard trigger of damage."""

    respond = [standard.Damage]

    def process(self, event: respond[0]):
        event.message()

        return []


class StdDeathPhase(StandardBeforeTrigger):
    """Standard trigger of death phase."""

    respond = [standard.DeathPhase]

    def process(self, event: respond[0]):
        result = []
        for death in event.deaths:
            if isinstance(death, Hero):
                result.append(standard.HeroDeath(self.game, death))
            elif isinstance(death, Minion):
                result.append(standard.MinionDeath(self.game, death))
            elif isinstance(death, Weapon):
                result.append(standard.WeaponDeath(self.game, death))
        return result


def add_standard_triggers(game):
    game.register_trigger(StdGameBegin(game))
    game.register_trigger(StdTurnBegin(game))
    game.register_trigger(StdTurnEnd(game))
    game.register_trigger(StdDrawCard(game))
    game.register_trigger(StdOnPlaySpell(game))
    game.register_trigger(StdSpellBlenderPhase(game))
    game.register_trigger(StdSpellText(game))
    game.register_trigger(StdAfterSpell(game))
    game.register_trigger(StdPreDamage(game))
    game.register_trigger(StdDamage(game))
    game.register_trigger(StdDeathPhase(game))
