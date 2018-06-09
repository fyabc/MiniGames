#! /usr/bin/python
# -*- coding: utf-8 -*-

"""Damage/healing bonus enchantments.

They will add bonuses to proposed damage or healing.

Examples:
    Enchantment granted by aura of "Prophet Velen".
    Enchantment granted by aura of "Fallen Hero".

[NOTE]: DH bonus enchantments acts different from normal enchantments.

    They do not use ``apply`` and ``apply_imm`` methods, use ``get_bonus_value`` instead.
"""

from .enchantment import Enchantment, AuraEnchantment
from ...utils.game import DHBonusEventType, Type, DHBonusType

__author__ = 'fyabc'


class DHBonusMixin:
    """The mixin class of damage/healing bonus enchantments and aura enchantments."""

    event_types = [DHBonusEventType.Invalid]
    source_types = [Type.Invalid]
    bonus_types = [DHBonusType.Invalid]

    def get_bonus_value(self):
        """Get the bonus value (number of add or double)."""
        raise NotImplementedError()


class DHBonusEnchantment(DHBonusMixin, Enchantment):
    """The class of damage/healing bonus enchantments."""


class DHBonusAuraEnchantment(DHBonusMixin, AuraEnchantment):
    """The class of damage/healing bonus aura enchantments."""


__all__ = [
    'DHBonusType',
    'DHBonusMixin',
    'DHBonusEnchantment',
    'DHBonusAuraEnchantment',
]
