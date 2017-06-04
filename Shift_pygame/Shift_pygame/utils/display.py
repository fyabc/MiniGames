#! /usr/bin/python
# -*- coding: utf-8 -*-

import pygame

from ..config import *
from ..support.vector import Vector2

__author__ = 'fyabc'


def update():
    pygame.display.update()


def get_font(font_size=FontSize, font_name=FontName):
    return pygame.font.Font(font_name, font_size)


def get_image(image_name):
    return pygame.image.load(os.path.join(ImagePath, image_name)).convert_alpha()


def to_color(color):
    if isinstance(color, str):
        return Colors[color]
    if isinstance(color, bool):
        return Bool2Color[color]
    return color


def get_text(text, foreground, background=None, font_size=FontSize, font_name=FontName):
    foreground = to_color(foreground)
    background = to_color(background)
    return get_font(font_size, font_name).render(text, True, foreground, background)


def relative2physic(loc):
    x, y = loc

    if x > 1 or y > 1:
        return loc

    return Vector2(x * ScreenWidth, y * ScreenHeight)
