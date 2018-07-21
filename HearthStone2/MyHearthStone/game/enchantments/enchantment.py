#! /usr/bin/python
# -*- coding: utf-8 -*-

"""Base classes of enchantment."""

from ..game_entity import GameEntity, IndependentEntity, make_property
from ...utils.game import Type, Zone

__author__ = 'fyabc'


class Enchantment(GameEntity):
    """Base class of enchantment.

    Information from <https://hearthstone.gamepedia.com/Enchantment>:
        An enchantment, also known as a buff or debuff, is a special effect gained by a minion,
        or in rarer occasions by a weapon.

        Most enchantments belong to minions while on the battlefield.
        However, some enchantments affect cards of other types, and some are active while in the player's hand.
        Enchantments may be granted permanently, or temporarily by an aura.

    Some notes:
    1. Copied from <https://hearthstone.gamepedia.com/Advanced_rulebook#Auras>:
        Despite not visually updating, enchantments take effect the moment they are created.
    """

    data = {
        'type': Type.Enchantment,
        'aura': False,
    }

    def __init__(self, game, target: IndependentEntity, **kwargs):
        """Create a new enchantment.

        When an enchantment is initialized, it is attached to its target and is ALWAYS in play.

        :param game:
        :param target: The target of this enchantment.
        :type target: IndependentEntity
        :param kwargs:
            :keyword oop: int, order of play
            :keyword player_id: int, player id of the creator
                [NOTE]: This is different from ``self.owner.player_id``.
        :type kwargs: dict
        """
        super().__init__(game)
        self.target = target

        # The creator of this enchantment.
        self.creator = kwargs.pop('creator', None)
        # TODO: Is this correct? Or make this a property that always trace the recent oop value of target?
        self.oop = kwargs.pop('oop', None if self.creator is None else self.creator.oop)

        target.add_enchantment(self)

        self.set_zp(Zone.Play, player_id=kwargs.pop(
            'player_id', None if self.creator is None else self.creator.player_id))

        # Apply the enchantment immediately.
        self.apply_imm()

    def _repr(self):
        return super()._repr()

    def set_zp(self, zone=None, player_id=None):
        # TODO: Specific behaviour of enchantment: (or needn't?)
        # Only have two zones: Play & RFG.
        if zone not in (Zone.Play, Zone.RFG):
            raise ValueError("Enchantment can be only moved to 'Play' or 'RFG', but try to move to {!r}.".format(
                Zone.Idx2Str[zone]))
        super().set_zp(zone, player_id)

    # Indicate that this enchantment is granted from an aura or not.
    aura = make_property('aura', setter=False)

    @property
    def order(self):
        """The order in enchantment list. Sorted in increase order."""
        return (1 if self.aura else 0), self.oop

    def apply_imm(self):
        """Apply this enchantment to the attached target immediately after attachment.

        This method usually set some permanent attributes, such as taunt, stealth, etc.
        When apply an enchantment of "set health to x", this method also need to set the damage value to 0.

        Subclasses should overwrite this method, and they should only modify the attributes directly.
        For example, ``self.taunt = True``.
        """
        pass

    def apply(self):
        """Apply this enchantment to the attached target in aura updates.

        This method usually set some attributes that will be recalculated in aura updates, such as attack, health
        and mana cost.

        Subclasses should overwrite this method, and they should only modify ``self.aura_tmp``.
        For example, ``self.aura_tmp['attack'] *= 2``.
        """
        pass

    @classmethod
    def from_card(cls, creator: GameEntity, *args, **kwargs):
        """Create an enchantment from the creator.

        This is the recommended method to create an enchantment.

        This method will set the oop and player id of the enchantment from the creator.
        """

        kwargs['creator'] = creator
        kwargs['oop'] = creator.oop
        kwargs['player_id'] = creator.player_id
        enc = cls(*args, **kwargs)

        return enc

    def detach(self, remove_from_target=False):
        """Detach the enchantment from its target.
        This enchantment is removed from play.

        This method or target itself will remove this enchantment from its target,
        decided by kwarg ``remove_from_target``.
        """
        if remove_from_target:
            self.target.remove_enchantment(self)
        self.set_zp(Zone.RFG, player_id=None)


class AuraEnchantment(Enchantment):
    """Enchantments that granted by auras.

    These enchantments are "temporary", and will be moved to the end of the enchantment list when the aura update.
    """

    data = {
        'aura': True,
    }

    def __init__(self, game, target: IndependentEntity, source, **kwargs):
        super().__init__(game, target, **kwargs)
        self._source = source

    @property
    def source(self):
        """The source aura of this enchantment."""
        return self._source


__all__ = [
    'Enchantment',
    'AuraEnchantment',
]
