#! /usr/bin/python
# -*- encoding: utf-8 -*-

from ..config import *
from ..utils.display import get_text
from .handler import EventHandler

__author__ = 'fyabc'


class ActiveText(EventHandler):
    def __init__(self, game, text, loc, fg, bg, font_size=FontSize, font_name=FontName, visible=True):
        super().__init__(game, True)

        self.image = get_text(text, fg, bg, font_size, font_name)
        self.loc = loc
        self.visible = visible

    def __contains__(self, item):
        rect = self.image.get_rect()
        rect.center = self.loc
        return rect.collidepoint(item)

    def _on_mouse_down_1(self, game, event):
        pass

    def _on_mouse_up_1(self, game, event):
        pass

    def draw(self, surface=None):
        if not self.visible:
            return

        surface = self.game.main_window if surface is None else surface

        rect = self.image.get_rect()
        rect.center = self.loc
        surface.blit(self.image, rect)
