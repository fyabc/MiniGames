#! /usr/bin/python
# -*- coding: utf-8 -*-

from cocos.cocosnode import CocosNode
from cocos.draw import Canvas, parameter, Line

__author__ = 'fyabc'


class Rect(Canvas):
    """The CocosNode to draw a rectangle."""
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

    def set_rect_attr(self, name, value):
        """Set rect attributes, also set the dirty flag.

        Common code ``r.rect.center = p`` will not set the dirty flag, use ``r.set_rect_attr('center', p)`` instead.
        """
        setattr(self.rect, name, value)
        self._dirty = True


class Circle(CocosNode):
    def draw(self, *args, **kwargs):
        # TODO
        pass


__all__ = [
    'Rect',
    'Line',
]
