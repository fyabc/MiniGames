#! /usr/bin/python
# -*- encoding: utf-8 -*-

from ..handler import EventHandler

__author__ = 'fyabc'


class Element(EventHandler):
    def __init__(self, game):
        super().__init__(game)

    def get_area(self):
        pass

    def __contains__(self, item):
        return False
