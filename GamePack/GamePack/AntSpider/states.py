#! /usr/bin/python
# -*- encoding: utf-8 -*-

from .brain import BrainState

__author__ = 'fyabc'


class AntExploring(BrainState):
    """Ant randomly exploring the target."""

    def __init__(self, ant):
        super().__init__(ant)

    def check_conditions(self):
        pass


class AntSeeking(BrainState):
    """Ant get the target and seeking it."""

    def __init__(self, ant):
        super().__init__(ant)

    def check_conditions(self):
        pass
