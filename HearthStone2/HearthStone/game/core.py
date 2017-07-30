#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'fyabc'


from .event_engine import EventEngine


class Game:
    """The core game system. Include an engine and some game data."""

    def __init__(self):
        self.engine = EventEngine(self)
