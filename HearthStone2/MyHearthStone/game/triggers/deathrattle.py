#! /usr/bin/python
# -*- coding: utf-8 -*-

from .trigger import Trigger
from ..events import standard

__author__ = 'fyabc'


class DrTrigger(Trigger):
    """Trigger of deathrattle.

    [NOTE]: This type of triggers are active in any zone.
    Copied from <https://hearthstone.gamepedia.com/Advanced_rulebook#Mid-Phase_removal_and_triggers>::

        Rule MPR2: Deathrattles are an exception to rule MPR1 - despite being triggers, they can resolve in any zone,
        including Play, Hand, Graveyard and Deck.

    [NOTE]: The behaviour of deathrattle triggers are different from normal:
        1. They are not attached to its owner or its target.
        2. In death creation step, they are registered into the core.
        3. Remove it from core after processing.

        This design is to reduce the number of deathrattle triggers, since they are active in all zones.
        This design need to reserve "dr_trigger" and "dr_list" data when resetting tags between zones.
    """
    respond = [standard.DeathEvent]

    def __init__(self, game, owner, target, dr_fn, reg_fn=None, data=None):
        """

        :param game:
        :param owner: The entity who create this trigger.
        :param target: The target entity of this trigger.
        :param dr_fn: The deathrattle function called in processing.
            Call signature: (this_trigger, death_event) -> event_list
            You can reference the target entity as ``this_trigger.target``.
        :param reg_fn: The function called when registered in death creation step.
            Some deathrattles may need to remember the state of the target here.
            Call signature: (this_trigger) -> None
        """
        super().__init__(game, owner)
        self.target = target
        self.dr_fn = dr_fn
        self.reg_fn = reg_fn
        self.data = {} if data is None else data

    def copy(self, new_owner=None, new_target=None):
        result = super().copy(new_owner=new_owner)
        if new_target is not None:
            result.target = new_target
        return result

    def register_before_death(self):
        self.game.register_trigger(self)
        if self.reg_fn is not None:
            self.reg_fn(self)

    def process(self, event: respond[0]):
        # Only process the death of the target.
        if event.owner is not self.target:
            return []
        result = self.dr_fn(self, event) if self.dr_fn is not None else []

        # Remove myself from core after processing.
        self.game.remove_trigger(self)
        return result

    @classmethod
    def create(cls, game, **kwargs):
        """Create a deathrattle trigger.

        TODO: Make the creation of deathrattle more convenient.

        Usage::

            # Used as deathrattle owned by an entity
            class M(Minion):
                def __init__(self, game, player_id):
                    super().__init__(game, player_id)
                    self.dr_trigger = std_triggers.DrTrigger.create(
                        self.game, owner=self,
                        dr_fn=lambda trigger, event: [],
                        reg_fn=lambda trigger: None,
                        data={},
                    )

            # Used as deathrattle granted by enchantment
            TODO: Add example

        :param game:
        :param kwargs:
            :keyword owner:
            :keyword target:
            :keyword dr_fn:
            :keyword reg_fn:
            :keyword data:
            :keyword owned:
        :return:
        :rtype: DrTrigger
        """
        dr_fn = kwargs.pop('dr_fn', None)
        reg_fn = kwargs.pop('reg_fn', None)
        data = kwargs.pop('data', None)
        owner = kwargs['owner']
        if kwargs.pop('owned', True):
            return cls(game, owner, owner, dr_fn, reg_fn, data)
        else:
            target = kwargs['target']
            return cls(game, owner, target, dr_fn, reg_fn, data)
