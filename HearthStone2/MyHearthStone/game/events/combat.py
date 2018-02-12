#! /usr/bin/python
# -*- coding: utf-8 -*-

"""Combat events.

Copied from https://hearthstone.gamepedia.com/Advanced_rulebook#Combat:
    When you order a minion to attack another minion, the following Sequence takes place:
    (As with other Sequences, if the attacker or defender leaves play for any reason,
    the current Phase will finish resolving but the Sequence will end early afterwards.

        1. If you have Gladiator's Longbow or Candleshot at the start of Combat Sequence,
        you are Immune in the whole Sequence.

        2. **Combat Preparation Phase**: A Proposed Attack Event is resolved. If the defender changes,
        another Proposed Attack Event is created and placed in this Phase's Event Queue
        after the current Proposed Attack Event. (It will begin to resolve when the current Proposed Attack Event
        finishes resolving.) Finally, an Attack Event is resolved. Additionally, the attacker will lose Stealth.

        3. Hearthstone checks for win/loss/draw.

        4. **Combat Phase**: Damage is dealt simultaneously in the order (attack, counterattack) and resolved.
        The attacker's weapon loses durability (unless prevented due to the weapon being Immune).
        An After Attack Event is resolved even if 0 damage was dealt to the defender.
        Note that after Patch 9.2.0.21517 after attack triggers can only work if they're valid when the Sequence starts.

        5. Hearthstone checks for win/loss/draw.

    The subjects of Combat are the attacker and defender.
    Even if the attacker or defender (or both) is mortally wounded or leaves play,
    triggers that ask what the current attacker/defender is will continue to be able to queue and resolve
    (assuming their other conditions are satisfied.)

    **Proposed Attack Event**: See https://hearthstone.gamepedia.com/Advanced_rulebook#Proposed_Attack_Event.

    **Attack Event**: See https://hearthstone.gamepedia.com/Advanced_rulebook#Attack_Event.

    **After Attack Event**: See https://hearthstone.gamepedia.com/Advanced_rulebook#After_Attack_Event.
"""

from .event import Event, Phase

__author__ = 'fyabc'


class PrepareCombat(Phase):
    """The prepare combat phase. It contains ``ProposedAttack`` and ``Attack`` events."""

    def __init__(self, game, combat):
        super().__init__(game, None)
        self.combat = combat

    def _repr(self):
        return super()._repr(attacker=self.combat.attacker, defender=self.combat.defender)


class Combat(Phase):
    def __init__(self, game, combat):
        super().__init__(game, None)
        self.combat = combat

    def _repr(self):
        return super()._repr(attacker=self.combat.attacker, defender=self.combat.defender)


class ProposedAttack(Event):
    def __init__(self, game, combat):
        super().__init__(game, None)
        self.combat = combat

    def _repr(self):
        return super()._repr(attacker=self.combat.attacker, defender=self.combat.defender)


class Attack(Event):
    def __init__(self, game, attacker, defender):
        super().__init__(game, None)
        self.attacker = attacker
        self.defender = defender

    def _repr(self):
        return super()._repr(attacker=self.attacker, defender=self.defender)


class AfterAttack(Event):
    pass


def combat_events(game, attacker, defender):
    return []
