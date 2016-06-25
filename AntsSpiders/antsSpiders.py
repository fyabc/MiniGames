# -*- coding: utf-8 -*-

__author__ = 'fyabc'

import pygame

from AntsSpiders.entities import World, WorldEntity


class Leaf(WorldEntity):
    Image = None

    @staticmethod
    def loadImage():
        if Leaf.Image is None:
            Leaf.Image = pygame.image.load('leaf.png').convert_alpha()
        return Leaf.Image

    def __init__(self, world):
        super(Leaf, self).__init__('leaf', world)
        self.image = self.loadImage()


class Spider(WorldEntity):
    Image = None

    @staticmethod
    def loadImage():
        if Spider.Image is None:
            Spider.Image = pygame.image.load('spider.jpg').convert_alpha()
        return Spider.Image

    def __init__(self, world):
        super(Spider, self).__init__('spider', world)
        self.image = self.loadImage()
