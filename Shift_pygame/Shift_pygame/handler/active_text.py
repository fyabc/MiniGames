#! /usr/bin/python
# -*- encoding: utf-8 -*-

import pygame.locals

from ..config import *
from ..utils.display import get_text, relative2physic
from .handler import EventHandler
from ..element.text import Text

__author__ = 'fyabc'


class ActiveText(EventHandler, Text):
    def __init__(self, game, scene,
                 text, loc, fg_bg=(False, True), font_size=FontSize, font_name=FontName,
                 visible=True,
                 on_mouse_up=None):
        """

        :param game:
        :param scene:
        :param text:
        :param loc:
        :param fg_bg:
        :param font_size:
        :param font_name:
        :param visible:
        :param on_mouse_up: callable or None.
            Call it on mouse up event.
            [NOTE] parameters: text(self), scene, event, previous_scene_id, *args
            return: next_scene_id, *next_args
        """

        super().__init__(game, {
            (pygame.locals.MOUSEBUTTONDOWN, 1),
        })
        Text.__init__(self, game, scene, text, loc, fg_bg, font_size, font_name, visible, 0)

        self.clicked = False

        # The default setting of active text:
        # Clicked color is inverted common color.
        self.text = text
        self.fg_bg = fg_bg
        self.font = font_size, font_name

        self.add_action((pygame.locals.MOUSEBUTTONDOWN, 1), self.on_mouse_down_1)
        self.on_mouse_up = (lambda text_, scene_, event_, pre_sid, *args: None) if on_mouse_up is None else on_mouse_up

    def __contains__(self, item):
        rect = self.image.get_rect()
        rect.center = self.loc
        return rect.collidepoint(item)

    def invert(self):
        self.clicked = not self.clicked
        self.fg_bg = [not c for c in self.fg_bg]
        self.image = get_text(self.text, *self.fg_bg, *self.font)

    def on_mouse_down_1(self, scene, event, pre_sid, *args):
        self.invert()

    def on_mouse_up_1(self, scene, event, pre_sid, *args):
        self.invert()
        return self.on_mouse_up(self, scene, event, pre_sid, *args)
