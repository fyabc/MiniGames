#! /usr/bin/python
# -*- encoding: utf-8 -*-

import argparse

import pygame
import pygame.locals

from ..basic.runner import PygameRunner
from ..utils.constant import Colors, FPS

__author__ = 'fyabc'


Keymap = {
    'exit': [pygame.locals.K_q, ],
    'start': [pygame.locals.K_s, ],
    'pause': [pygame.locals.K_p, ],
    'reset': [pygame.locals.K_r, ],
    'left': [pygame.locals.K_LEFT, ],
    'right': [pygame.locals.K_RIGHT, ],
    'up': [pygame.locals.K_UP, ],
    'down': [pygame.locals.K_DOWN, ],
}


class Snake(PygameRunner):
    # Some color and style constants.
    BGColor = Colors['black']
    EdgeColor = Colors['white']
    LineColor = Colors['gray18']
    SnakeColor = Colors['green']
    SnakeHeadColor = Colors['red']
    FoodColor = Colors['yellow']
    TextColor = Colors['white']
    
    LineWidth = 1
    
    def main_loop(self):
        pass


def real_main(options):
    pass


def build_parser():
    parser = argparse.ArgumentParser(description='A simple implementation of Snake.')

    return parser


def main():
    parser = build_parser()

    options = parser.parse_args()

    real_main(options)
