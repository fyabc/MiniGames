#! /usr/bin/python
# -*- coding: utf-8 -*-

"""Play events.

Playing a spell: See https://hearthstone.gamepedia.com/Advanced_rulebook#Playing_a_spell.

Playing a weapon: See https://hearthstone.gamepedia.com/Advanced_rulebook#Playing_a_weapon.

Playing a Death Knight hero: See https://hearthstone.gamepedia.com/Advanced_rulebook#Playing_a_Death_Knight_hero.

Playing/Summoning a minion: See https://hearthstone.gamepedia.com/Advanced_rulebook#Playing.2Fsummoning_a_minion.

"""

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


class Summon(Event):
    def __init__(self, game, minion, loc, player_id=None):
        super().__init__(game, minion)
        self.loc = loc
        self.player_id = player_id

    @property
    def minion(self):
        return self.owner

    def _repr(self):
        return super()._repr(P=self.player_id, minion=self.owner, loc=self.loc)


class OnPlayMinion(OnPlay):
    def __init__(self, game, minion, loc, target, player_id=None):
        super().__init__(game, None)
        self.target = target
        self.summon_event = Summon(self.game, minion, loc, player_id)

    @property
    def player_id(self):
        return self.summon_event.player_id

    @property
    def minion(self):
        return self.summon_event.minion

    def _repr(self):
        return super()._repr(P=self.summon_event.player_id, minion=self.summon_event.minion,
                             loc=self.summon_event.loc, target=self.target)


class BattlecryPhase(Phase):
    def __init__(self, game, summon_event, target):
        super().__init__(game, summon_event)
        self.summon_event = summon_event
        self.target = target

    @property
    def player_id(self):
        return self.summon_event.player_id

    @property
    def minion(self):
        return self.summon_event.minion

    def _repr(self):
        return super()._repr(P=self.summon_event.player_id, minion=self.summon_event.minion, target=self.target)


class AfterPlayMinion(AfterPlay):
    skip_5_steps = True

    def __init__(self, game, summon_event):
        super().__init__(game, None)
        self.summon_event = summon_event

    @property
    def player_id(self):
        return self.summon_event.player_id

    @property
    def minion(self):
        return self.summon_event.minion

    def _repr(self):
        return super()._repr(P=self.summon_event.player_id, minion=self.summon_event.minion)


class AfterSummon(Phase):
    def __init__(self, game, summon_event):
        super().__init__(game, None)
        self.summon_event = summon_event

    @property
    def player_id(self):
        return self.summon_event.player_id

    @property
    def minion(self):
        return self.summon_event.minion

    def _repr(self):
        return super()._repr(P=self.summon_event.player_id, minion=self.summon_event.minion)


def pure_summon_events(game, minion, to_player, loc, from_player=None, from_zone=None):
    """Utility for merely summon a minion.

    :param game: The game of the minion.
    :param minion: Minion id (generate) or ``Minion`` instance (forced play from hand or deck).
    :param to_player: The to player id.
    :param loc: integer or 'last', The location of the minion to summon.
    :param from_player: The from player id, None if the minion is generated.
    :param from_zone: The from zone id, None if the minion is generated.
    :return: event list.
    """

    if from_zone is None:
        minion, status = game.generate(to_player, Zone.Play, loc, minion)
    else:
        minion, status = game.move(from_player, from_zone, minion, to_player, Zone.Play, loc)
    success = status['success']
    to_index = status['to_index']

    if success:
        summon_event = Summon(game, minion, to_index, to_player)
        game.summon_events.add(summon_event)

        # [NOTE]: move it to ``Game.move``?
        minion.oop = game.inc_oop()

        return [AfterSummon(game, summon_event)]
    else:
        return []
