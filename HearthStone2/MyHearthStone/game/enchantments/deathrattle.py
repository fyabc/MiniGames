#! /usr/bin/python
# -*- coding: utf-8 -*-

from .enchantment import Enchantment
from ..game_entity import make_property

__author__ = 'fyabc'


class DrEnchantment(Enchantment):
    """The deathrattle enchantment."""

    data = {
        'dr_trigger': None,
    }

    def __init__(self, game, target, **kwargs):
        self.dr_trigger = kwargs.pop('dr_trigger', None)
        super().__init__(game, target, **kwargs)

    dr_trigger = make_property('dr_trigger', default=None)

    def apply_imm(self):
        # Add the deathrattle trigger into dr_list.
        if self.dr_trigger is not None:
            self.target.dr_list.append(self.dr_trigger)
