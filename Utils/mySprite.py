# -*- coding: utf-8 -*-

import pygame

__author__ = 'fyabc'


class MySprite(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super(MySprite, self).__init__(*groups)

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class MyGroup(pygame.sprite.Group):
    def __init__(self, *sprites):
        super(MyGroup, self).__init__(*sprites)

    def draw(self, surface):
        sprites = self.sprites()
        for sprite in sprites:
            sprite.draw(surface)
        self.lostsprites = []
