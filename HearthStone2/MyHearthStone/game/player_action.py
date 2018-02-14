#! /usr/bin/python
# -*- coding: utf-8 -*-

from .events import standard

__author__ = 'fyabc'


class PlayerAction:
    """"""

    def __init__(self, game):
        self.game = game

    def phases(self):
        """Extract phases from this player action."""

        raise NotImplementedError('implemented by subclasses')


class TurnEnd(PlayerAction):
    """"""

    def __init__(self, game, player_id=None):
        super().__init__(game)
        self.player_id = game.current_player if player_id is None else player_id

    def phases(self):
        return [
            standard.EndOfTurn(self.game), 'check_win',
            standard.BeginOfTurn(self.game), 'check_win',
            standard.DrawCard(self.game, None), 'check_win',    # The card drawer is determined by the next player.
        ]


class Concede(PlayerAction):
    """May be useless?"""

    def __init__(self, game, player_id=None):
        super().__init__(game)
        self.player_id = game.current_player if player_id is None else player_id

    def phases(self):
        return [
            standard.HeroDeath(self.game, self.game.players[self.player_id].hero), 'check_win',
        ]


class PlaySpell(PlayerAction):
    """"""

    def __init__(self, game, spell, target, player_id=None):
        super().__init__(game)
        self.spell = spell
        self.target = target
        self.player_id = game.current_player if player_id is None else player_id

    def phases(self):
        return [
            standard.OnPlaySpell(self.game, self.spell, self.target, self.player_id),
            standard.SpellBenderPhase(self.game, self.spell, self.target, self.player_id),
            standard.SpellText(self.game, self.spell, self.target, self.player_id),
            standard.AfterSpell(self.game, self.spell, self.target, self.player_id),
            'check_win',
        ]


class PlayWeapon(PlayerAction):
    """"""

    def __init__(self, game, weapon, target, player_id=None):
        super().__init__(game)
        self.weapon = weapon
        self.target = target
        self.player_id = game.current_player if player_id is None else player_id

    def phases(self):
        return []


class PlayMinion(PlayerAction):
    """The action to play a minion.

    Some Notes:
        1. Playing Lord Jaraxxus initially summons him as a minion, before his Battlecry transforms him into a hero
            who then takes over from the playing hero. (in `BattlecryPhase`)
    """

    def __init__(self, game, minion, loc, target, player_id=None):
        super().__init__(game)
        self.minion = minion
        self.loc = loc
        self.target = target
        self.player_id = game.current_player if player_id is None else player_id

    def phases(self):
        opm = standard.OnPlayMinion(self.game, self.minion, self.loc, self.target, self.player_id)
        return [
            opm,
            standard.BattlecryPhase(self.game, opm.summon_event, opm.target),
            standard.AfterPlayMinion(self.game, opm.summon_event),
            standard.AfterSummon(self.game, opm.summon_event),
            'check_win',
        ]


class ToAttack(PlayerAction):
    """"""

    def __init__(self, game, attacker, defender):
        super().__init__(game)
        self.attacker = attacker
        self.defender = defender

    def phases(self):
        atk_event = standard.Attack(self.game, self.attacker, self.defender)
        return [
            standard.PrepareCombat(self.game, atk_event),
            'check_win',
            standard.Combat(self.game, atk_event),
            'check_win',
        ]


class UseHeroPower(PlayerAction):
    """"""

    def __init__(self, game, target, player_id):
        super().__init__(game)
        self.target = target
        self.player_id = game.current_player if player_id is None else player_id

    def phases(self):
        return []
