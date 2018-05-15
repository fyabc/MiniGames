#! /usr/bin/python
# -*- coding: utf-8 -*-

from ..events import standard
from .trigger import StandardBeforeTrigger
from ...utils.constants import version_le

__author__ = 'fyabc'

# todo: Complete combat triggers.


class StdPrepareCombat(StandardBeforeTrigger):
    """Standard trigger of prepare-combat.

    Copied from Advanced Rulebook::

        1. If you have Gladiator's Longbow or Candleshot at the start of Combat Sequence,
        you are Immune in the whole Sequence.[156][157]

        2. **Combat Preparation Phase**: A Proposed Attack Event is resolved.
        If the defender changes, another Proposed Attack Event is created and placed in this Phase's Event Queue
        after the current Proposed Attack Event. (It will begin to resolve when the current Proposed Attack Event
        finishes resolving.)
        Finally, an Attack Event is resolved.
        Additionally, the attacker will lose Stealth.
    """
    respond = [standard.PrepareCombat]

    def process(self, event: respond[0]):
        ae = event.attack_event
        pae = standard.ProposedAttack(event.game, ae)

        # Remove stealth.
        if version_le("11.0.0"):
            # After patch 11.0.0, Minions now only break Stealth when attacking.
            # Damage dealt by card abilities, such as Knife Juggler's knife throw, no longer breaks Stealth.
            if ae.attacker.stealth:
                ae.attacker.stealth = False
            # FIXME: Need to add a ``LoseStealth`` event?

        return [
            pae,
            ae,
        ]


class StdCombat(StandardBeforeTrigger):
    """The standard trigger of Combat phase.

    Increase attack number of attacker (where?).

    todo:
    Damage order: See **Ordering of damage in the Combat Phase** in
        https://hearthstone.gamepedia.com/Advanced_rulebook#Combat.
    """
    respond = [standard.Combat]

    def process(self, event: respond[0]):
        g, a, d = event.game, event.attacker, event.defender

        a.inc_n_attack()

        return (standard.damage_events(g, a, d, a.attack) +
                standard.damage_events(g, d, a, d.attack) +
                [standard.AfterAttack(event.game, event.attack_event)])


class StdAttack(StandardBeforeTrigger):
    respond = [standard.Attack]

    def process(self, event: respond[0]):
        # todo: The attacker will lose stealth.
        return []
