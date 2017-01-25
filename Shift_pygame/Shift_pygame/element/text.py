#! /usr/bin/python
# -*- coding: utf-8 -*-

from ..config import *
from .element import Element
from ..utils.display import get_text

__author__ = 'fyabc'


class Text(Element):
    def __init__(self, game, scene,
                 text, loc, fg_bg=(False, True), font_size=FontSize, font_name=FontName,
                 visible=True, angle=0):
        super().__init__(game, scene, loc, angle, visible, 'center')

        self.text = text
        self.fg_bg = fg_bg
        self.font_size = font_size
        self.font_name = font_name

        self.image = get_text(text, *fg_bg, font_size, font_name)

    def set_text(self, text):
        self.text = text
        self.image = get_text(self.text, *self.fg_bg, self.font_size, self.font_name)
