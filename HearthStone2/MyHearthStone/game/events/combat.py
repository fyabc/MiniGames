#! /usr/bin/python
# -*- coding: utf-8 -*-

"""Combat events.

Sequence details: See https://hearthstone.gamepedia.com/Advanced_rulebook#Combat.

**Proposed Attack Event**: See https://hearthstone.gamepedia.com/Advanced_rulebook#Proposed_Attack_Event.

**Attack Event**: See https://hearthstone.gamepedia.com/Advanced_rulebook#Attack_Event.

**After Attack Event**: See https://hearthstone.gamepedia.com/Advanced_rulebook#After_Attack_Event.
"""

from .event import Event, Phase

__author__ = 'fyabc'


class PrepareCombat(Phase):
    """The prepare combat phase. It contains ``ProposedAttack`` and ``Attack`` events."""

    def __init__(self, game, attack_event):
        super().__init__(game, None)
        self.attack_event = attack_event

    @property
    def attacker(self):
        return self.attack_event.attacker

    @property
    def defender(self):
        return self.attack_event.defender

    def _repr(self):
        return super()._repr(attacker=self.attack_event.attacker, defender=self.attack_event.defender)


class Combat(Phase):
    def __init__(self, game, attack_event):
        super().__init__(game, None)
        self.attack_event = attack_event

    @property
    def attacker(self):
        return self.attack_event.attacker

    @property
    def defender(self):
        return self.attack_event.defender

    def _repr(self):
        return super()._repr(attacker=self.attack_event.attacker, defender=self.attack_event.defender)


class ProposedAttack(Event):
    """The event of proposed attack.

    This event does not have standard triggers.

    Copied from Advanced Rulebook:

        Triggers on the Proposed Attack Event include those that can change the defender, cause the attacker to become
        mortally wounded or leave play, and so on.

        At the start of resolving a Proposed Attack Event, triggers queue based on the defender at that moment, and
        will remain in the queue even if the defender changes.

        When the defender changes, a new Proposed Attack Event is inserted into the Combat Preparation Phase's Event
        Queue after the currently resolving one. (It will therefore resolve once the current Proposed Attack Event
        finishes resolving, and therefore use the defender at that point in time.)

        (As a reminder: Queuing conditions are only required to be true when the Event they trigger on starts to
        resolve, whereas trigger conditions are only required to be true when the trigger resolves.)
    """
    def __init__(self, game, attack_event):
        super().__init__(game, None)
        self.attack_event = attack_event

    @property
    def attacker(self):
        return self.attack_event.attacker

    @property
    def defender(self):
        return self.attack_event.defender

    def _repr(self):
        return super()._repr(attacker=self.attack_event.attacker, defender=self.attack_event.defender)


class Attack(Event):
    """The event of attack.

    Copied from Advanced Rulebook:

        Triggers on the Attack Event include those that need to occur only once the final defender is known, or those
        that do not significantly affect the game state. The Attack Event is only resolved if the previous Proposed
        Attack Event did not change the defender.
    """
    def __init__(self, game, attacker, defender):
        super().__init__(game, None)
        self.attacker = attacker
        self.defender = defender

    def _repr(self):
        return super()._repr(attacker=self.attacker, defender=self.defender)


class AfterAttack(Event):
    """The event of after-attack.

    This event does not have standard triggers.

    Copied from Advanced Rulebook:

        An After Attack Event is resolved as long as the attack was successful, even if it dealt 0 damage.

        (Note that unlike other triggers that go 'after' something, such as Rumbling Elemental and Djinni of Zephyrs,
        the After Attack Event is resolved in the same Phase, not a later Phase, as the combat damage, meaning death
        processing is not done in-between.)
    """
    def __init__(self, game, attack_event):
        super().__init__(game, None)
        self.attack_event = attack_event

    @property
    def attacker(self):
        return self.attack_event.attacker

    @property
    def defender(self):
        return self.attack_event.defender

    def _repr(self):
        return super()._repr(attacker=self.attack_event.attacker, defender=self.attack_event.defender)
