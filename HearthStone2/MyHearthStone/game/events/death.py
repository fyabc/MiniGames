#! /usr/bin/python
# -*- coding: utf-8 -*-

from .event import Event, Phase
from ...utils.game import Type

__author__ = 'fyabc'


def _push_death_cache(game, event_owner):
    """Push death events into death event cache.

    See <https://hearthstone.gamepedia.com/Advanced_rulebook#Death_Event_Cache> for details.

    Values: (entity_id, player_id, turn_number)
    """
    game.death_cache.append((event_owner.id, event_owner.player_id, game.n_turns))


class DeathPhase(Phase):
    """The death phase, contains some death events."""
    def __init__(self, game, death_events):
        super().__init__(game, None)
        self.deaths = death_events

    def _repr(self):
        return super()._repr(deaths=self.deaths)

    def do(self):
        return self.deaths


class HeroDeath(Event):
    def _repr(self):
        return super()._repr(hero=self.owner)

    def do(self):
        owner = self.owner
        _push_death_cache(self.game, owner)
        owner.play_state = False
        return owner.run_deathrattle()


class MinionDeath(Event):
    """The event of minion death."""
    def __init__(self, game, death, location):
        super().__init__(game, death)
        self.location = location

    # TODO: OOP exception:
    # Most things use the oop order of ``self.owner``, but Kel'Thuzad use the oop order of the death event self.
    # So need to create own oop of this event? Or implement it use death event cache?

    def _repr(self):
        return super()._repr(minion=self.owner, loc=self.location)

    def do(self):
        _push_death_cache(self.game, self.owner)
        return self.owner.run_deathrattle(location=self.location)


class WeaponDeath(Event):
    def _repr(self):
        return super()._repr(weapon=self.owner)

    def do(self):
        _push_death_cache(self.game, self.owner)
        return self.owner.run_deathrattle()


def create_death_event(game, death, location=None):
    type_ = death.type

    if type_ == Type.Hero:
        return HeroDeath(game, death)
    elif type_ == Type.Minion:
        return MinionDeath(game, death, location)
    elif type_ == Type.Weapon:
        return WeaponDeath(game, death)
    else:
        raise ValueError('Unknown death type {}'.format(type_))
