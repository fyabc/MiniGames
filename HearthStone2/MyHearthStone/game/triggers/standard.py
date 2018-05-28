#! /usr/bin/python
# -*- coding: utf-8 -*-

"""Standard triggers.

This module includes useful trigger APIs, and used for creating new cards.
"""

from ..events import standard
from .trigger import Trigger

__author__ = 'fyabc'


class DetachOnTurnEnd(Trigger):
    """The trigger commonly used in "Temporary" enchantments.

    This trigger will let its owner being detached on the end of turn.
    """
    respond = [standard.EndOfTurn]

    def process(self, event: respond[0]):
        self.owner.detach(remove_from_target=True)
        return []


__all__ = [
    'Trigger',
    'DetachOnTurnEnd',
]
