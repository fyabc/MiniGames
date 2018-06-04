#! /usr/bin/python
# -*- coding: utf-8 -*-

from ...utils.message import entity_message
from ...utils.game import Zone, AuraType

__author__ = 'fyabc'


class Aura:
    """Aura (also called ongoing effect).

    Information from <https://hearthstone.gamepedia.com/Ongoing_effect>:
        Ongoing effects are minion, weapon, and boss Hero Power abilities which grant special effects
        on an ongoing basis. Ongoing effects are often referred to as auras, particularly those which grant
        temporary enchantments to other targets.
    """

    # TODO: This class is like the ``Trigger`` class, which has its active zones, and will update when changing zones.

    # Aura type.
    type = AuraType.AttackHealth

    # Zones that this aura is active.
    zones = [Zone.Play]

    def __init__(self, game, owner):
        self.game = game
        self.owner = owner

        # Automatically add it to its owner.
        owner.add_aura(self)

    @property
    def oop(self):
        return self.owner.oop

    @property
    def order(self):
        """The order of granted enchantments in enchantment list.

        Used by searching the enchantment in the list.

        See ``Enchantment.order`` for more details."""
        return 1, self.oop

    def prepare_update(self):
        """Prepare the update of this aura, called by aura update methods of ``Game``.

        In this method, you can do some useful calculations that are available during this update, for example,
        the location of the owner. It can avoid the recalculation for many times.
        """
        pass

    def process_entity(self, entity, **kwargs):
        """Process the entity, called by aura update methods of ``Game``.

        :param entity: The entity to be processed.
        :param kwargs: Some useful information, such as the location of the entity.
        :return:
        """

        match = self.check_entity(entity, **kwargs)

        # If not match, remove the previous granted enchantment on the entity if it exists.
        if not match:
            entity.remove_enchantment_by_aura(self)
            return

        # If match, grant the enchantment to the entity (or do nothing if it already exists).
        exist_enc = entity.get_enchantment_by_aura(self)
        if exist_enc is None:
            self.grant_enchantment(entity, **kwargs)
        else:
            self.modify_exist_enchantment(entity, exist_enc, **kwargs)

    def check_entity(self, entity, **kwargs):
        """Check if this entity match the condition of this aura."""
        raise NotImplementedError()

    def grant_enchantment(self, entity, **kwargs):
        """Grant the enchantment on this entity."""
        raise NotImplementedError()

    def modify_exist_enchantment(self, entity, enchantment, **kwargs):
        """Modify the enchantment that has been already granted to the entity.

        In default and the most cases, this method do nothing.

        An example that need to override this method:
            "Aura: Your other minions have +1 attack, your other minion with charge have +2 attack instead."
            If one friendly minion gain charge, it need to modify the exist enchantment.
        """
        pass

    def detach_granted_enchantments(self):
        for entity in self.game.get_all_entities():
            entity.remove_enchantment_by_aura(self)

    def __repr__(self):
        return self._repr()

    def _repr(self, **kwargs):
        kwargs['owner'] = self.owner
        return entity_message(self, kwargs, prefix='%')
