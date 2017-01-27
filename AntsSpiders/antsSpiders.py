# -*- coding: utf-8 -*-

from random import randint

import pygame
import pygame.locals

from Utils.vector2 import Vector2
from AntsSpiders.config import *
from AntsSpiders.entities import AntsSpidersWorld, Leaf, Spider, Ant

__author__ = 'fyabc'

MainWindow = None
Timer = None


def run():
    world = AntsSpidersWorld()
    w, h = SCREEN_SIZE

    for i in range(ANT_NUMBER):
        ant = Ant(world)
        ant.brain.changeState('exploring')

    for i in range(INIT_LEAF_NUMBER):
        leaf = Leaf(None)
        leaf.location = Vector2(randint(10, w - 10), randint(10, h - 10))
        if leaf.location.distance(NEST_LOC) > NEST_RADIUS * LEAF_OCCUR_RANGE:
            world.addEntity(leaf)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                print('Bye!')
                running = False

        timePassed = Timer.tick(TIME_PASSED)

        if randint(1, SPIDER_FREQ) == 2:    # 平均每xx个tick出现一个spider
            newSpider = Spider(world)
            newSpider.location = Vector2(-50, randint(0, h))
            # nestx, nesty = NEST_LOC
            # newSpider.destination = Vector2(w + 50, randint(nesty - NEST_SIZE, nesty + NEST_SIZE))
            newSpider.destination = Vector2(w + 50, randint(0, h))

        if randint(1, LEAF_FREQ) == 2:      # 平均每xx个tick出现一个leaf（只在巢穴外出现）
            leaf = Leaf(None)
            leaf.location = Vector2(randint(10, w - 10), randint(10, h - 10))
            if leaf.location.distance(NEST_LOC) > NEST_RADIUS * LEAF_OCCUR_RANGE:
                world.addEntity(leaf)

        if randint(1, CLEAR_FREQ) == 2:
            world.clearDeath(MainWindow)

        world.step(timePassed / 1000.0)
        world.draw(MainWindow)
        pygame.display.update()


def main():
    global MainWindow, Timer

    pygame.init()

    MainWindow = pygame.display.set_mode(SCREEN_SIZE)
    Timer = pygame.time.Clock()
    pygame.display.set_caption("Ants and Spiders")

    run()

    pygame.quit()


if __name__ == '__main__':
    main()
