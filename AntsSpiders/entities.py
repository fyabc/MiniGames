# -*- coding: utf-8 -*-

__author__ = 'fyabc'

import pygame

from StateMachine.simpleBrain import State, Brain


class World(pygame.sprite.Group):
    def __init__(self):
        super(World, self).__init__()


class Ant(pygame.sprite.Sprite):
    def __init__(self):
        super(Ant, self).__init__()
        
        
class Spider(pygame.sprite.Sprite):
    def __init__(self):
        super(Spider, self).__init__()
