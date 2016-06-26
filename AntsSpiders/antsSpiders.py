# -*- coding: utf-8 -*-

__author__ = 'fyabc'

import pygame

from AntsSpiders.config import SCREEN_SIZE
from AntsSpiders.entities import World, Leaf, Spider, Ant

MainWindow = None
Timer = None


def run():
    world = World()
    Ant(world)

    world.draw(MainWindow)
    pygame.display.update()


def main():
    global MainWindow, Timer

    pygame.init()

    MainWindow = pygame.display.set_mode(SCREEN_SIZE)
    Timer = pygame.time.Clock()

    run()

    pygame.quit()


if __name__ == '__main__':
    main()
