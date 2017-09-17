#! /usr/bin/python
# -*- coding: utf-8 -*-

"""Standard events."""

from .event import Event

__author__ = 'fyabc'


class BeginOfGame(Event):
    def __init__(self, game):
        super().__init__(game, None)
        self._oop = game.inc_oop()

    @property
    def oop(self):
        return self._oop

    def message(self):
        super().message(first_player=self.game.current_player)


class BeginOfTurn(Event):
    def __init__(self, game):
        super().__init__(game, None)
        self._oop = game.inc_oop()

    @property
    def oop(self):
        return self._oop

    def message(self):
        super().message(n=self.game.n_turns, player=self.game.current_player)


class EndOfTurn(Event):
    def __init__(self, game):
        super().__init__(game, None)
        self._oop = game.inc_oop()

    @property
    def oop(self):
        return self._oop

    def message(self):
        super().message(n=self.game.n_turns, player=self.game.current_player)


class DrawCard(Event):
    def __init__(self, game, owner, player_id=None):
        super().__init__(game, owner)
        self.player_id = player_id if player_id is not None else self.game.current_player
        self.card = None

    def message(self):
        super().message(P=self.player_id, card=self.card)


class OnPlay(Event):
    pass


class OnPlaySpell(OnPlay):
    def __init__(self, game, spell, target, player_id=None):
        super().__init__(game, spell)
        self.target = target
        self.player_id = player_id if player_id is not None else self.game.current_player

    @property
    def spell(self):
        return self.owner

    def message(self):
        super().message(P=self.player_id, spell=self.owner, target=self.target)


class SpellBenderPhase(Event):
    """The special phase for the spell bender.

    [NOTE]: The Death Creation Step and Summon Resolution Step is skipped following this Phase.     # todo
    """

    def __init__(self, game, spell, target, player_id=None):
        super().__init__(game, spell)
        self.target = target
        self.player_id = player_id if player_id is not None else self.game.current_player

    @property
    def spell(self):
        return self.owner

    def message(self):
        super().message(P=self.player_id, spell=self.owner, target=self.target)


class SpellText(OnPlay):
    def __init__(self, game, spell, target, player_id=None):
        super().__init__(game, spell)
        self.target = target
        self.player_id = player_id if player_id is not None else self.game.current_player

    @property
    def spell(self):
        return self.owner

    def message(self):
        super().message(P=self.player_id, spell=self.owner, target=self.target)


class AfterSpell(OnPlay):
    def __init__(self, game, spell, target, player_id=None):
        super().__init__(game, spell)
        self.target = target
        self.player_id = player_id if player_id is not None else self.game.current_player

    @property
    def spell(self):
        return self.owner

    def message(self):
        super().message(P=self.player_id, spell=self.owner, target=self.target)


class PreDamage(Event):
    def __init__(self, game, damage):
        super().__init__(game, damage.owner)
        self.damage = damage

    def message(self):
        super().message(source=self.owner, target=self.damage.target, value=self.damage.value)


class Damage(Event):
    def __init__(self, game, owner, target, value):
        super().__init__(game, owner)
        self.target = target
        self.value = value

    def message(self):
        super().message(source=self.owner, target=self.target, value=self.value)


def damage_events(game, owner, target, value):
    """Utility to get damage event sequences."""

    damage = Damage(game, owner, target, value)
    return [
        PreDamage(game, damage),
        damage,
    ]


class DeathPhase(Event):
    def __init__(self, game, deaths):
        super().__init__(game, None)
        self.deaths = deaths

    def message(self):
        super().message(deaths=self.deaths)


class HeroDeath(Event):
    def message(self):
        super().message(hero=self.owner)


class MinionDeath(Event):
    def message(self):
        super().message(minion=self.owner)


class WeaponDeath(Event):
    def message(self):
        super().message(weapon=self.owner)


def game_begin_standard_events(game):
    return [BeginOfGame(game), BeginOfTurn(game), DrawCard(game, None)]
