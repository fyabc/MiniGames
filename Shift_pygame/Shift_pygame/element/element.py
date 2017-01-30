#! /usr/bin/python
# -*- encoding: utf-8 -*-

import pygame

from ..config import Anchor
from ..utils.display import get_image, relative2physic

__author__ = 'fyabc'


class Element:
    """Element in Shift world."""

    SharedImages = {}

    def __init__(self, game, scene, loc, angle=0, visible=True, anchor=Anchor.center):
        self.game = game
        self.scene = scene
        self.image = None
        self.loc = relative2physic(loc)
        self.anchor = Anchor.str2anchor(anchor)
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

        # FIXME: The pygame rotate is counterclockwise, so set the negative value!!!
        rotated_image = pygame.transform.rotate(self.image, -self.angle)
        rotated_image_rect = rotated_image.get_rect()

        # [NOTE] Use `exec` to apply the anchor.
        exec('rotated_image_rect.{} = self.loc'.format(self.anchor))

        surface.blit(rotated_image, rotated_image_rect)

    def rotate(self, angle):
        self.angle += angle
