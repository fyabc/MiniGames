#! /usr/bin/python
# -*- coding: utf-8 -*-

from cocos.draw import Canvas, parameter

__author__ = 'fyabc'


class Rect(Canvas):
    # todo: Support filled rect.

    rect = parameter()
    color = parameter()
    width = parameter()

    def __init__(self, rect, color, width=1):
        super().__init__()
        self.rect = rect
        self.color = color
        self.width = width

    def render(self):
        self.set_color(self.color)
        self.set_stroke_width(self.width)
        self.move_to(self.rect.bottomleft)
        self.line_to(self.rect.topleft)
        self.line_to(self.rect.topright)
        self.line_to(self.rect.bottomright)
        self.line_to(self.rect.bottomleft)


__all__ = [
    'Rect',
]
