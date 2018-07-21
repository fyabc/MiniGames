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
        self._kw = kwargs
        super().__init__(game, target, **kwargs)

    dr_trigger = make_property('dr_trigger', default=None)

    def apply_imm(self):
        # Create the deathrattle trigger.
        from ..triggers.deathrattle import DrTrigger
        self.dr_trigger = DrTrigger.create(
            self.game, owner=self.creator,
            target=self.target,
            dr_fn=self._kw.get('dr_fn', None),
            reg_fn=self._kw.get('reg_fn', None),
            data=self._kw.get('data', None),
            owned=False,
        )
        del self._kw

        # Add the deathrattle trigger into dr_list.
        self.target.dr_list.append(self.dr_trigger)


__all__ = [
    'DrEnchantment',
]
