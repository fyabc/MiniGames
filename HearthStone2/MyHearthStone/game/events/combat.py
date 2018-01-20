#! /usr/bin/python
# -*- coding: utf-8 -*-

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
