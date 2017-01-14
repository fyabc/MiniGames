#! /usr/bin/python
# -*- coding: utf-8 -*-

import pygame

from .element import Element

__author__ = 'fyabc'


class ShiftElement(Element):
    def __init__(self, game, scene, cell_loc, image_name, angle=0, visible=True):
        super().__init__(game, scene, scene.physic_loc(cell_loc), angle, visible)
        self._cell_loc = cell_loc
        self.set_image(image_name)

    @property
    def cell_loc(self):
        return self._cell_loc

    @cell_loc.setter
    def cell_loc(self, new_loc):
        self._cell_loc = new_loc
        self.loc = self.scene.physic_loc(new_loc)

    def rotate_window(self, angle):
        """When the window is rotated, call this method to change the element.

        angle must be multiple of 90.
        """
        pass


class Door(ShiftElement):
    SharedImages = {}

    def __init__(self, game, scene, cell_loc, bg=False, angle=0, visible=True):
        super().__init__(game, scene, cell_loc, 'door{}.png'.format(int(bg)), angle, visible)


class Hero(ShiftElement):
    SharedImages = {}
    
    def __init__(self, game, scene, cell_loc, bg=False, angle=0, visible=True):
        super().__init__(game, scene, cell_loc, 'character{}.png'.format(int(bg)), angle, visible)
