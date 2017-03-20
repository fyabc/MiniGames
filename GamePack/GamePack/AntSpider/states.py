#! /usr/bin/python
# -*- encoding: utf-8 -*-

from random import random

from .brain import BrainState
from .constants import *

__author__ = 'fyabc'


class AntExploring(BrainState):
    """Ant randomly exploring the target."""

    def __init__(self, ant, **kwargs):
        super().__init__(ant)
        self.random_dest_prob = kwargs.pop('random_dest_prob', AntRandomDestinationProb)
        self.see_leaf_range = kwargs.pop('see_leaf_range', AntSeeLeafRange)

    def _random_destination(self):
        self.owner.location = self.owner.world.random_location()

    def do_actions(self):
        if random() <= self.random_dest_prob:
            self._random_destination()

    def check_conditions(self):
        # If ant sees a leaf, go to the seeking state.
        leaf = self.owner.world.get_close_entity('Leaf', self.owner.location, self.see_leaf_range)
        if leaf:
            self.owner.leaf_id = leaf.id
            return AntSeeking

        # If the ant sees a spider attacking the base, go to hunting state
        # todo

        return None


class AntSeeking(BrainState):
    """Ant get the target and seeking it."""

    def __init__(self, ant):
        super().__init__(ant)

    def check_conditions(self):
        pass
