#! /usr/bin/python
# -*- coding: utf-8 -*-

"""Standard triggers for death phases and events.

[NOTE]: In death phase, the dead entity have been **REMOVED FROM PLAY**.
"""

from ..card import Minion, Weapon
from ..events import standard
from ..hero import Hero
from .trigger import StandardBeforeTrigger

__author__ = 'fyabc'


class StdDeathPhase(StandardBeforeTrigger):
    """Standard trigger of death phase."""

    respond = [standard.DeathPhase]

    def process(self, event: respond[0]):
        result = []
        for death in event.deaths:
            if isinstance(death, Hero):
                result.append(standard.HeroDeath(self.game, death))
            elif isinstance(death, Minion):
                result.append(standard.MinionDeath(self.game, death))
            elif isinstance(death, Weapon):
                result.append(standard.WeaponDeath(self.game, death))
        return result


def _push_death_event(game, event_owner):
    """Push death events into event handlers.

    See https://hearthstone.gamepedia.com/Advanced_rulebook#Death_Event_Cache for details.

    Values: (entity_id, player_id, turn_number)
    """
    game.death_cache.append((event_owner.id, event_owner.player_id, game.n_turns))


class StdHeroDeath(StandardBeforeTrigger):
    """Standard trigger of hero death."""

    respond = [standard.HeroDeath]

    def process(self, event: respond[0]):
        owner = event.owner
        _push_death_event(self.game, owner)
        owner.play_state = False
        return owner.run_deathrattle()


class StdMinionDeath(StandardBeforeTrigger):
    """Standard trigger of minion death."""

    respond = [standard.MinionDeath]

    def process(self, event: respond[0]):
        _push_death_event(self.game, event.owner)
        return event.owner.run_deathrattle()


class StdWeaponDeath(StandardBeforeTrigger):
    """Standard trigger of weapon death."""

    respond = [standard.WeaponDeath]

    def process(self, event: respond[0]):
        _push_death_event(self.game, event.owner)
        return event.owner.run_deathrattle()
