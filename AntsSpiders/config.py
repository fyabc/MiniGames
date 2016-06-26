# -*- coding: utf-8 -*-

__author__ = 'fyabc'

from pygame.colordict import THECOLORS as AllColors

SCREEN_SIZE = (640, 480)
BG_COLOR = AllColors['white']
NEST_COLOR = AllColors['lightgreen']
TEXT_COLOR = AllColors['blue']

NEST_LOC = (0, 0)
NEST_RADIUS = 100

# Ant configs.
RANDOM_DESTINATION_PROB = 20

SEE_LEAF_RANGE = 130.
SEE_SPIDER_RANGE = 100.
CARRY_RANGE = 5.

EXPLORING_SPEED_RANGE = (90, 150)
SEEKING_SPEED_RANGE = (140, 180)
