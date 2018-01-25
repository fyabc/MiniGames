#! /usr/bin/python
# -*- coding: utf-8 -*-

"""Standard triggers of play events."""

from ..events import standard
from .trigger import StandardBeforeTrigger
from ...utils.game import error_and_stop, Zone

__author__ = 'fyabc'


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

        player = self.game.players[event.player_id]

        # todo: Add effect of Cho'gall
        if player.displayed_mana() < event.spell.cost:
            error_and_stop(self.game, event, 'You do not have enough mana!')
            return []

        if not event.spell.check_target(event.target):
            error_and_stop(self.game, event, 'This is not a valid target!')
            return []

        if event.spell.data['secret']:
            if player.full(Zone.Secret):
                error_and_stop(self.game, event, 'I cannot have more secrets!')
                return []

            for card in player.get_zone(Zone.Secret):
                if card.data['id'] == event.spell.data['id']:
                    error_and_stop(self.game, event, 'I already have this secret!')
                    return []

        player.used_mana += event.spell.cost

        # [NOTE]: move it to ``Game.move``?
        event.spell.oop = self.game.inc_oop()

        tz = Zone.Graveyard
        if event.spell.data['secret']:
            tz = Zone.Secret

        self.game.move(event.player_id, Zone.Hand, event.spell, event.player_id, tz, 'last')

        return []


class StdSpellBlenderPhase(StandardBeforeTrigger):
    """Standard trigger of SpellBlenderPhase (may be useless?)."""

    respond = [standard.SpellBenderPhase]

    def process(self, event: respond[0]):
        return []


class StdSpellText(StandardBeforeTrigger):
    """Standard trigger of SpellText."""

    respond = [standard.SpellText]

    def process(self, event: respond[0]):
        return event.spell.run(event.target)


class StdAfterSpell(StandardBeforeTrigger):
    """Standard trigger of AfterSpell (may be useless?)."""

    respond = [standard.AfterSpell]

    def process(self, event: respond[0]):
        return []


class StdOnPlayMinion(StandardBeforeTrigger):
    """Standard trigger of OnPlayMinion."""

    respond = [standard.OnPlayMinion]

    def process(self, event: respond[0]):
        """Process the OnPlayMinion event.

        :param event: The event to be processed.
        :return: new event list.
        """

        player = self.game.players[event.player_id]

        # todo: Add effect of Seadevil Stinger
        if player.displayed_mana() < event.minion.cost:
            error_and_stop(self.game, event, 'You do not have enough mana!')
            return []

        if not event.minion.check_target(event.target):
            error_and_stop(self.game, event, 'This is not a valid target!')
            return []

        if player.full(Zone.Play):
            error_and_stop(self.game, event, 'You cannot have more minions!')
            return []

        player.used_mana += event.minion.cost

        self.game.summon_events.add(standard.Summon(self.game, event.minion, event.player_id))

        # [NOTE]: move it to `Game.move`?
        event.minion.oop = self.game.inc_oop()

        self.game.move(event.player_id, Zone.Hand, event.minion, event.player_id, Zone.Play, event.loc)

        return []


class StdOnBattlecry(StandardBeforeTrigger):
    """Standard trigger of BattlecryPhase."""

    respond = [standard.BattlecryPhase]

    def process(self, event: respond[0]):
        # todo: Add effects of Brann Bronzebeard.

        return event.minion.battlecry(event.target)


class StdAfterPlayMinion(StandardBeforeTrigger):
    """Standard trigger of AfterPlayMinion."""

    respond = [standard.AfterPlayMinion]


class StdAfterSummon(StandardBeforeTrigger):
    """Standard trigger of AfterSummon."""

    respond = [standard.AfterSummon]
