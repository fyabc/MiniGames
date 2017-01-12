#! /usr/bin/python
# -*- coding: utf-8 -*-

import os

import pygame

from ..config import *

__author__ = 'fyabc'


def update():
    pygame.display.update()


def get_font(font_size=FontSize, font_name=FontName):
    return pygame.font.Font(font_name, font_size)


def get_image(image_name):
    return pygame.image.load(os.path.join(ImagePath, image_name)).convert_alpha()
