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
        # [NOTE] The angle here need to be multiply of 90 (is it must be?).

        self.game = game
        self.scene = scene

        # [NOTE] self.image should be set by subclasses.
        self.image = None
        self.loc = relative2physic(loc)
        self.anchor = Anchor.str2anchor(anchor)
        self._angle = angle
        self.visible = visible

        # The rotated image. Recalculate when changing the angle.
        # Used for get the `rect` attribute.
        # [NOTE] the `draw` method use this rotated image to draw the element,
        #     so you should ensure that it is update at any time.
        self._rotated_image = None

    def set_image(self, image_attr):
        """set the `image` attribute.

        This method should be called by any subclasses.

        [NOTE] This method should also set the `_rotated_image` method.

        :param image_attr: The image attributes, default is the image name.
        :return: None
        """
        if image_attr not in self.SharedImages:
            self.SharedImages[image_attr] = get_image(image_attr)

        self.image = self.SharedImages[image_attr]

        self._set_rotated_image()

    @property
    def rect(self):
        """Get the rect of the element (from the rotated image)."""

        if self._rotated_image is None:
            self._set_rotated_image()
        rotated_image_rect = self._rotated_image.get_rect()

        # [NOTE] Use `exec` to apply the anchor.
        exec('rotated_image_rect.{} = self.loc.to_tuple()'.format(self.anchor))

        return rotated_image_rect

    def _set_rotated_image(self, flip=False):
        if flip:
            tmp_image = pygame.transform.flip(self.image, True, False)
        else:
            tmp_image = self.image

        if self.image is not None:
            # FIXME: The pygame rotate is counterclockwise, so set the negative value!!!
            self._rotated_image = pygame.transform.rotate(tmp_image, -self.angle)

    @property
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, value):
        """Set the new angle, and change the rotated image."""

        self._angle = value

        self._set_rotated_image()

    def draw(self, surface=None):
        if not self.visible:
            return

        surface = self.game.main_window if surface is None else surface

        if self._rotated_image is None:
            self._set_rotated_image()

        surface.blit(self._rotated_image, self.rect)

    def rotate(self, angle):
        self.angle += angle
