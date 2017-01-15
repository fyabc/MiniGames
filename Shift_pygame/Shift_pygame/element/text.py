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

        self.image = get_text(text, *fg_bg, font_size, font_name)
