#! /usr/bin/python
# -*- encoding: utf-8 -*-

from .handler import EventHandler

__author__ = 'fyabc'


class ActiveText(EventHandler):
    def __init__(self, game):
        super().__init__(game, True)
