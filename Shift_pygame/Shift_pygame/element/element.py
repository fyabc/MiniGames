#! /usr/bin/python
# -*- encoding: utf-8 -*-

import pygame

from ..utils.display import get_image, relative2physic

__author__ = 'fyabc'


class Element:
    """Element in Shift world."""

    SharedImages = {}

    def __init__(self, game, scene, loc, angle=0, visible=True, anchor='center'):
        self.game = game
        self.scene = scene
        self.image = None
        self.loc = relative2physic(loc)
        self.anchor = anchor        # todo: To be implemented
        self.angle = angle
        self.visible = visible

    def set_image(self, image_name):
        if image_name not in self.SharedImages:
            self.SharedImages[image_name] = get_image(image_name)

        self.image = self.SharedImages[image_name]
        # rect = self.image.get_rect()
        # rect.center = self.loc

    @property
    def rect(self):
        return self.image.get_rect()

    def draw(self, surface=None):
        if not self.visible:
            return

        surface = self.game.main_window if surface is None else surface

        rotated_image = pygame.transform.rotate(self.image, self.angle)
        rotated_image_rect = rotated_image.get_rect()
        rotated_image_rect.center = self.loc
        surface.blit(rotated_image, rotated_image_rect)

    def rotate(self, angle):
        self.angle += angle
