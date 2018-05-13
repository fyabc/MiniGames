#! /usr/bin/python
# -*- coding: utf-8 -*-

"""Standard triggers of play events."""

from ..events import standard
from .trigger import StandardBeforeTrigger
from ...utils.game import Zone

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
        player.spend_mana(event.spell.cost)

        # [NOTE]: move it to `Game.move`?
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
        player.spend_mana(event.minion.cost)

        se = event.summon_event
        self.game.summon_events.add(se)

        # [NOTE]: move it to `Game.move`?
        event.minion.oop = self.game.inc_oop()

        _, status = self.game.move(se.player_id, Zone.Hand, event.minion, se.player_id, Zone.Play, se.loc)

        return status['events']


class StdOnBattlecry(StandardBeforeTrigger):
    """Standard trigger of BattlecryPhase."""

    respond = [standard.BattlecryPhase]

    def process(self, event: respond[0]):
        # todo: Add effects of Brann Bronzebeard.

        return event.minion.run_battlecry(event.target)


class StdAfterPlayMinion(StandardBeforeTrigger):
    """Standard trigger of AfterPlayMinion."""

    respond = [standard.AfterPlayMinion]


class StdSummon(StandardBeforeTrigger):
    """Standard trigger of Summon.

    This trigger process something both for played minions or pure-summoned minions, such as set exhaustion.
    """

    respond = [standard.Summon]

    def process(self, event: respond[0]):
        minion = event.minion
        minion.init_attack_status()
        return []


class StdAfterSummon(StandardBeforeTrigger):
    """Standard trigger of AfterSummon."""

    respond = [standard.AfterSummon]
