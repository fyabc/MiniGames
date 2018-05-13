#! /usr/bin/python
# -*- coding: utf-8 -*-

"""Base classes of enchantment."""

from ..game_entity import GameEntity, make_property
from ...utils.game import Type

__author__ = 'fyabc'


class Enchantment(GameEntity):
    """Base class of enchantment.

    Information from <https://hearthstone.gamepedia.com/Enchantment>:
        An enchantment, also known as a buff or debuff, is a special effect gained by a minion,
        or in rarer occasions by a weapon.

        Most enchantments belong to minions while on the battlefield.
        However, some enchantments affect cards of other types, and some are active while in the player's hand.
        Enchantments may be granted permanently, or temporarily by an aura.
    """

    data = {
        'type': Type.Enchantment,
        'aura': False,
    }

    def __init__(self, game, target):
        super().__init__(game)
        self.target = target

    aura = make_property('aura', setter=False)

    @property
    def order(self):
        """The order in enchantment list. Sorted in increase order."""
        return (1 if self.aura else 0), self.oop

    def apply(self):
        """Apply this enchantment to the attached target."""
        pass

    @classmethod
    def from_card(cls, creator: GameEntity, *args, **kwargs):
        """Create an enchantment from the creator.

        This method will set the oop of enchantment as the enchantment of the creator.
        """

        enc = cls(*args, **kwargs)
        enc.oop = creator.oop

        return enc


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
