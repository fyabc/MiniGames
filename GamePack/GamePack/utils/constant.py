#! /usr/bin/python
# -*- encoding: utf-8 -*-

import sys

from pygame.colordict import THECOLORS as Colors

WINDOWS = sys.platform == 'win32'

ScreenSize = (640, 480)
FPS = 50

if WINDOWS:
    FontName = 'C:/Windows/Fonts/msyh.ttc'
else:
    FontName = None

__author__ = 'fyabc'
