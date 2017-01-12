#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'fyabc'


class Group:
    def __init__(self, game, *elements, **kwargs):
        self.game = game

        ordered = kwargs.pop('ordered', False)

        if ordered:
            self.elements = list(elements)
        else:
            self.elements = set(elements)

    def draw(self, surface=None):
        surface = self.game.main_window if surface is None else surface

        for element in self.elements:
            element.draw(surface)

    def __iter__(self):
        return iter(self.elements)
