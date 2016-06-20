# -*- coding: utf-8 -*-

__author__ = 'fyabc'

from random import randint

import pygame

from AntsSpiders.config import *
from StateMachine.simpleBrain import State, Brain
from Utils.mySprite import MySprite, MyGroup


class AntExploring(State):
    def __init__(self, ant, seeLeafRange=130., seeSpiderRange=100.):
        super(AntExploring, self).__init__('exploring')
        self.ant = ant
        self.seeLeafRange = seeLeafRange
        self.seeSpiderRange = seeSpiderRange

    def randomDestination(self):
        w, h = SCREEN_SIZE
        self.ant.destination = [randint(0, w), randint(0, h)]

    def doActions(self):
        if randint(1, 20) == 1:
            self.randomDestination()

    def checkConditions(self):
        # if ant sees a leaf, go to the seeking state.
        leaf = None


class World(MyGroup):
    def __init__(self):
        super(World, self).__init__()


class Ant(MySprite):
    def __init__(self, world, image):
        super(Ant, self).__init__()
        self.world = world
        self.image = image

    def draw(self, surface):
        super(Ant, self).draw(surface)
        
        
class Spider(MySprite):
    def __init__(self, world, image):
        super(Spider, self).__init__()
        self.world = world
        self.image = image

    def draw(self, surface):
        super(Spider, self).draw(surface)
