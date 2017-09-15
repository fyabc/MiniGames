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
        super().message(player=self.game.current_player, card=self.card)


class PreDamage(Event):
    def __init__(self, game, owner, target, value):
        super().__init__(game, owner)
        self.target = target
        self.value = value

    def message(self):
        super().message(source=self.owner, target=self.target, value=self.value)


class Damage(Event):
    def __init__(self, game, owner, target, value):
        super().__init__(game, owner)
        self.target = target
        self.value = value

    def message(self):
        super().message(source=self.owner, target=self.target, value=self.value)


class MinionDeath(Event):
    def __init__(self, game, owner):
        super().__init__(game, owner)

    def message(self):
        super().message(minion=self.owner)


def game_begin_standard_events(game):
    return [BeginOfGame(game), BeginOfTurn(game), DrawCard(game, None)]
