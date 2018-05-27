#! /usr/bin/python
# -*- coding: utf-8 -*-

from .events import standard
from ..utils.message import entity_message

__author__ = 'fyabc'


class PlayerAction:
    """"""

    def __init__(self, game):
        self.game = game

    def _repr(self, **kwargs):
        __show_cls = kwargs.pop('__show_cls', True)
        return entity_message(self, kwargs, prefix='*', __show_cls=__show_cls)

    def __repr__(self):
        return self._repr()

    def phases(self):
        """Extract phases from this player action."""

        raise NotImplementedError('implemented by subclasses')


class ReplaceStartCard(PlayerAction):
    """"""

    def __init__(self, game, player_id, replace_list):
        super().__init__(game)
        self.player_id = player_id
        self.replace_list = replace_list

    def phases(self):
        return []

    def _repr(self):
        return super()._repr(P=self.player_id, replace=self.replace_list)


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

    def _repr(self):
        return super()._repr(P=self.player_id)


class Concede(PlayerAction):
    """May be useless?"""

    def __init__(self, game, player_id=None):
        super().__init__(game)
        self.player_id = game.current_player if player_id is None else player_id

    def phases(self):
        return [
            standard.HeroDeath(self.game, self.game.players[self.player_id].hero), 'check_win',
        ]

    def _repr(self):
        return super()._repr(P=self.player_id)


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

    def _repr(self):
        return super()._repr(P=self.player_id, spell=self.spell, target=self.target)


class PlayWeapon(PlayerAction):
    """"""

    def __init__(self, game, weapon, target, player_id=None):
        super().__init__(game)
        self.weapon = weapon
        self.target = target
        self.player_id = game.current_player if player_id is None else player_id

    def phases(self):
        return [
            standard.OnPlayWeapon(self.game, self.weapon, self.target, self.player_id),
            standard.EquipWeapon(self.game, self.weapon, self.target, self.player_id, is_played=True),
            standard.AfterPlayWeapon(self.game, self.weapon, self.player_id),
            'check_win',
        ]

    def _repr(self):
        return super()._repr(P=self.player_id, weapon=self.weapon, target=self.target)


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

    def _repr(self):
        return super()._repr(P=self.player_id, minion=self.minion, loc=self.loc, target=self.target)


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

    def _repr(self):
        return super()._repr(attacker=self.attacker, defender=self.defender)


class UseHeroPower(PlayerAction):
    """"""

    def __init__(self, game, target, player_id):
        super().__init__(game)
        self.target = target
        self.player_id = game.current_player if player_id is None else player_id

    def phases(self):
        hp_event = standard.HeroPowerPhase(self.game, self.game.get_player(self.player_id).hero_power, self.target)
        return [
            hp_event,
            standard.InspirePhase(self.game, hp_event),
            'check_win',
        ]

    def _repr(self):
        return super()._repr(P=self.player_id, target=self.target)


def process_special_pa(game, player_action):
    """Process special player actions.

    :param game:
    :param player_action:
    :return: Stop the processing of this action?
    """
    if isinstance(player_action, ReplaceStartCard):
        if game.state != game.GameState.WaitReplace:
            return False
        game.data['replaces'][player_action.player_id] = player_action.replace_list[:]
        if all(l is not None for l in game.data['replaces']):
            game.on_replace_done()
            return True
        else:
            return False
    else:
        return False
