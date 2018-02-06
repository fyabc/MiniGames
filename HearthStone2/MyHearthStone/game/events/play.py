#! /usr/bin/python
# -*- coding: utf-8 -*-

from .event import Event, Phase
from .utils import dynamic_pid_prop
from ...utils.game import Zone

__author__ = 'fyabc'


class OnPlay(Phase):
    pass


class AfterPlay(Phase):
    pass


class OnPlaySpell(OnPlay):
    def __init__(self, game, spell, target, player_id=None):
        super().__init__(game, spell)
        self.target = target
        self._player_id = player_id

    player_id = dynamic_pid_prop()

    @property
    def spell(self):
        return self.owner

    def _repr(self):
        return super()._repr(P=self.player_id, spell=self.owner, target=self.target)


class SpellBenderPhase(Phase):
    """The special phase for the spell bender."""

    skip_5_steps = True

    def __init__(self, game, spell, target, player_id=None):
        super().__init__(game, spell)
        self.target = target
        self._player_id = player_id

    player_id = dynamic_pid_prop()

    @property
    def spell(self):
        return self.owner

    def _repr(self):
        return super()._repr(P=self.player_id, spell=self.owner, target=self.target)


class SpellText(Phase):
    def __init__(self, game, spell, target, player_id=None):
        super().__init__(game, spell)
        self.target = target
        self._player_id = player_id

    player_id = dynamic_pid_prop()

    @property
    def spell(self):
        return self.owner

    def _repr(self):
        return super()._repr(P=self.player_id, spell=self.owner, target=self.target)


class AfterSpell(AfterPlay):
    def __init__(self, game, spell, target, player_id=None):
        super().__init__(game, spell)
        self.target = target
        self._player_id = player_id

    player_id = dynamic_pid_prop()

    @property
    def spell(self):
        return self.owner

    def _repr(self):
        return super()._repr(P=self.player_id, spell=self.owner, target=self.target)


class OnPlayWeapon(OnPlay):
    pass


class EquipWeapon(Phase):
    pass


class AfterPlayWeapon(AfterPlay):
    pass


class OnPlayMinion(OnPlay):
    def __init__(self, game, minion, loc, target, player_id=None):
        super().__init__(game, minion)
        self.loc = loc
        self.target = target
        self._player_id = player_id

    player_id = dynamic_pid_prop()

    @property
    def minion(self):
        return self.owner

    def _repr(self):
        return super()._repr(P=self.player_id, minion=self.owner, loc=self.loc, target=self.target)


class BattlecryPhase(Phase):
    def __init__(self, game, minion, loc, target, player_id=None):
        super().__init__(game, minion)
        self.loc = loc  # May be useless?
        self.target = target
        self._player_id = player_id

    player_id = dynamic_pid_prop()

    @property
    def minion(self):
        return self.owner

    def _repr(self):
        return super()._repr(P=self.player_id, minion=self.owner, target=self.target)


class AfterPlayMinion(AfterPlay):
    skip_5_steps = True

    def __init__(self, game, minion, player_id=None):
        super().__init__(game, minion)
        self._player_id = player_id

    player_id = dynamic_pid_prop()

    @property
    def minion(self):
        return self.owner

    def _repr(self):
        return super()._repr(P=self.player_id, minion=self.owner)


class AfterSummon(Phase):
    def __init__(self, game, minion, player_id=None):
        super().__init__(game, minion)
        self._player_id = player_id

    player_id = dynamic_pid_prop()

    @property
    def minion(self):
        return self.owner

    def _repr(self):
        return super()._repr(P=self.player_id, minion=self.owner)


class Summon(Event):
    def __init__(self, game, minion, player_id=None):
        super().__init__(game, minion)
        self._player_id = player_id

    player_id = dynamic_pid_prop()

    @property
    def minion(self):
        return self.owner

    def _repr(self):
        return super()._repr(P=self.player_id, minion=self.owner)


def pure_summon_events(game, minion, to_player, loc, from_player=None, from_zone=None):
    """Utility for merely summon a minion.

    :param game: The game of the minion.
    :param minion: Minion id (generate) or ``Minion`` instance (forced play from hand or deck).
    :param to_player: The to player id.
    :param loc: integer, The location of the minion to summon.
    :param from_player: The from player id, None if the minion is generated.
    :param from_zone: The from zone id, None if the minion is generated.
    :return: after summon event or None.
    """

    if from_zone is None:
        minion, success, _ = game.generate(to_player, Zone.Play, loc, minion)
    else:
        minion, success, _ = game.move(from_player, from_zone, minion, to_player, Zone.Play, loc)

    if success:
        game.summon_events.add(Summon(game, minion, to_player))

        # [NOTE]: move it to ``Game.move``?
        minion.oop = game.inc_oop()

        return AfterSummon(game, minion, to_player)
    else:
        return None
