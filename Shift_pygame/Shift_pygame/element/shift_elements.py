#! /usr/bin/python
# -*- coding: utf-8 -*-

import pygame

from ..config import *
from ..utils.display import get_font
from .element import Element

__author__ = 'fyabc'


class ShiftElement(Element):
    def __init__(self, game, scene, cell_loc, image_name, angle=0, visible=True, anchor=Anchor.center):
        super().__init__(game, scene, scene.physic_loc(cell_loc, anchor), angle, visible, anchor)
        self._cell_loc = cell_loc
        self.set_image(image_name)

    @property
    def cell_loc(self):
        return self._cell_loc

    @cell_loc.setter
    def cell_loc(self, new_loc):
        self._cell_loc = new_loc
        self.loc = self.scene.physic_loc(new_loc, self.anchor)

    def rotate_window(self, angle):
        """When the window is rotated, call this method to change the element.

        angle must be multiple of 90.
        """
        pass

    @classmethod
    def from_attributes(cls, game, scene, dynamic_object, default_anchor=Anchor.bottom):
        """Create the element from the dynamic object.

        Here is the default implementation.
        """

        # The anchor of door is bottom.
        cell_loc = dynamic_object.x, dynamic_object.y

        return cls(
            game, scene,
            cell_loc,
            bg=scene.level_data[cell_loc],
            angle=dynamic_object.direction,
            anchor=Anchor.rotate(default_anchor, dynamic_object.direction),
        )


class Door(ShiftElement):
    SharedImages = {}

    def __init__(self, game, scene, cell_loc, bg=False, angle=0, visible=True, anchor=Anchor.bottom):
        super().__init__(game, scene, cell_loc, 'door{}.png'.format(int(bg)), angle, visible, anchor)


class Trap(ShiftElement):
    SharedImages = {}

    def __init__(self, game, scene, cell_loc, bg=False, angle=0, visible=True, anchor=Anchor.bottom):
        super().__init__(game, scene, cell_loc, 'trap{}.png'.format(int(bg)), angle, visible, anchor)


class Hero(ShiftElement):
    SharedImages = {}
    
    def __init__(self, game, scene, cell_loc, bg=False, angle=0, visible=True):
        # [NOTE] The anchor of the hero is always bottom.
        super().__init__(game, scene, cell_loc, 'hero{}.png'.format(int(bg)), angle, visible, Anchor.bottom)

        # [NOTE] The state of the hero that determines the image of hero and the horizontal speed of hero.
        # self.state in {
        #     -2 : left running,
        #     -1 : left stopping,
        #     +1 : right stopping,
        #     +2 : right running,
        # }
        self.state = 0

        self.vertical_speed = 0.0
        self.bg = bg

    @classmethod
    def from_attributes(cls, game, scene, dynamic_object, default_anchor=Anchor.bottom):
        cell_loc = dynamic_object.x, dynamic_object.y

        return cls(
            game, scene,
            cell_loc,
            bg=scene.level_data[cell_loc],
        )

    def run_command(self, command):
        """Run command from level scene."""

        # todo: some methods for running commands from the level scene.

        print('%command =', command)


class ShiftText(ShiftElement):
    SharedImages = {}

    DefaultFontSize = 19

    def __init__(self, game, scene, text, cell_loc, bg=False, angle=0, visible=True, anchor=Anchor.center):
        super().__init__(game, scene, cell_loc, [bg, text], angle, visible, anchor)

    def set_image(self, image_attr):
        bg, text = image_attr

        self.image = get_font(self.DefaultFontSize).render(text, True, Bool2Color[not bg], Bool2Color[bg])
        self._set_rotated_image()
