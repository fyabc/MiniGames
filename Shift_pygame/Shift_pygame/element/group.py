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

    def __getitem__(self, item):
        if not self.ordered:
            raise TypeError('unordered group does not support indexing')
        return self.elements[item]

    @property
    def ordered(self):
        return isinstance(self.elements, list)

    def add(self, *elements):
        if self.ordered:
            for element in elements:
                self.elements.append(element)
        else:
            for element in elements:
                self.elements.add(element)

    def clear(self):
        self.elements.clear()
