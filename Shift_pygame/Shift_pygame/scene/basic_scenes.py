#! /usr/bin/python
# -*- coding: utf-8 -*-

from ..element.group import Group
from .scene import Scene

__author__ = 'fyabc'


class MainMenu(Scene):
    def __init__(self, game, scene_id):
        super().__init__(game, scene_id)

        self.active_group = Group(self.game)
        self.groups.append(self.active_group)

    def add_active_element(self, element):
        self.handlers.append(element)
        self.active_group.add(element)
