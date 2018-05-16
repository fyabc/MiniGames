#! /usr/bin/python
# -*- coding: utf-8 -*-

"""Base classes of enchantment."""

from ..game_entity import GameEntity, make_property
from ..zone_movement import move_map
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

    # [NOTE]: It seems that the movement of enchantments are different from other entities.
    # TODO: The movement of enchantments are different from other entities. How to unify them?

    data = {
        'type': Type.Enchantment,
        'aura': False,
    }

    def __init__(self, game, target: GameEntity, **kwargs):
        """Create a new enchantment.

        When an enchantment is initialized, it is attached to its target and is ALWAYS in play.

        :param game:
        :param target: The target of this enchantment.
        :type target: GameEntity
        :param kwargs:
            :keyword oop: int, order of play
        :type kwargs: dict

        [NOTE]: Do not forget to call ``move_map`` after initializing (auto called in ``from_card``).
        """
        super().__init__(game)
        self.target = target
        # TODO: Is this correct? Or make this a property that always trace the recent oop value of target?
        self.oop = kwargs.pop('oop', None)

        target.add_enchantment(self)

    aura = make_property('aura', setter=False)

    @property
    def zone(self):
        real_zone = self.data.get('zone')
        return real_zone if real_zone is not None else self.target.zone

    @property
    def order(self):
        """The order in enchantment list. Sorted in increase order."""
        return (1 if self.aura else 0), self.oop

    # TODO: Add ``apply_imm``?

    def apply(self):
        """Apply this enchantment to the attached target."""
        pass

    @classmethod
    def from_card(cls, creator: GameEntity, *args, **kwargs):
        """Create an enchantment from the creator.

        This is the recommended method to create an enchantment.

        This method will set the oop of enchantment as the enchantment of the creator.
        """

        kwargs['oop'] = creator.oop
        enc = cls(*args, **kwargs)
        move_map(Zone.Invalid, enc.zone)(enc)

        return enc

    def detach(self, remove_from_target=False):
        """Detach the enchantment from its target.
        This enchantment is removed from play.

        This method or target itself will remove this enchantment from its target,
        decided by kwarg ``remove_from_target``.
        """
        move_map(self.data['zone'], Zone.RFG)(self)
        if remove_from_target:
            self.target.remove_enchantment(self)


class Aura(Enchantment):
    """Aura (also called ongoing effect).

    Information from <https://hearthstone.gamepedia.com/Ongoing_effect>:
        Ongoing effects are minion, weapon, and boss Hero Power abilities which grant special effects
        on an ongoing basis. Ongoing effects are often referred to as auras, particularly those which grant
        temporary enchantments to other targets.
    """

    data = {
        'aura': True,
    }


__all__ = [
    'Enchantment',
    'Aura',
]
