#! /usr/bin/python
# -*- coding: utf-8 -*-

import pygame

from ..config import *

__author__ = 'fyabc'


def update(rectangle=None):
    pygame.display.update(rectangle)


def get_font(font_size=FontSize, font_name=FontName):
    return pygame.font.Font(font_name, font_size)


def get_physic_loc(logic_loc, anchor='center'):
    pass
