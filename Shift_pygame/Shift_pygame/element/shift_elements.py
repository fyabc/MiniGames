#! /usr/bin/python
# -*- coding: utf-8 -*-

import pygame

from ..config import *
from ..utils.basic import sign
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

        self.cell_loc = self.scene.rotated_location(*self.cell_loc, angle=(-angle + 360) % 360)
        self.angle = (self.angle - angle) % 360

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

        self.height = self.image.get_height()
        self.width = self.image.get_width()

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

        if command == 'left':
            self._set_rotated_image(flip=True)
            self.state = -2
        elif command == 'right':
            self._set_rotated_image(flip=False)
            self.state = +2
        elif command == 'left_stop':
            if self.state < 0:
                self.state = -1
        elif command == 'right_stop':
            if self.state > 0:
                self.state = +1
        elif command == 'jump':
            if self.vertical_speed == 0:
                self.vertical_speed = InitJumpSpeed
        elif command == 'enter':
            # todo
            pass
        elif command == 'shift':
            if self._can_shift():
                self.scene.shift_map()

    def _can_shift(self):
        # todo
        return True

    def rotate_window(self, angle):
        # todo: special operations for heroes.
        pass

    def update(self, fps):
        cw, ch = self.scene.cell_width, self.scene.cell_height

        # calculate new horizontal location
        if abs(self.state) == 2:
            self.loc.x += sign(self.state) * HorizontalSpeed * fps

        rect = self.rect.copy()

        if self.state == -2:
            if self.hit_left(rect):
                self.loc.x = rect.right // cw * cw + self.width / 2     # [NOTE]

        if self.state == +2:
            if self.hit_right(rect):
                self.loc.x = rect.right // cw * cw - self.width / 2

        # calculate new vertical location
        self.loc.y += self.vertical_speed * fps

        rect = self.rect.copy()

        if self.vertical_speed >= 0:
            if self.hit_floor(rect):
                self.vertical_speed = 0
                self.loc.y = rect.bottom // ch * ch
            else:
                if self.vertical_speed < MaxDownSpeed:
                    self.vertical_speed += G
        else:
            if self.hit_ceil(rect):
                self.vertical_speed = 0
                self.loc.y = rect.bottom // ch * ch + self.height       # [NOTE]
            else:
                self.vertical_speed += G

    def hit_left(self, rect=None):
        rect = self.rect.copy() if rect is None else rect

        logic_tl = self.scene.logic_loc(rect.topleft, strict=True)
        logic_bl = self.scene.logic_loc((rect.bottomleft[0], rect.bottomleft[1] - 1), strict=True)

        return rect.left <= 0 or (logic_tl is not None and self.scene.get_color(*logic_tl) != self.bg) or \
            (logic_bl is not None and self.scene.get_color(*logic_bl) != self.bg)

    def hit_right(self, rect=None):
        rect = self.rect.copy() if rect is None else rect

        logic_tr = self.scene.logic_loc(rect.topright, strict=True)
        logic_br = self.scene.logic_loc((rect.bottomright[0], rect.bottomright[1] - 1), strict=True)

        return rect.right >= ScreenWidth or (logic_tr is not None and self.scene.get_color(*logic_tr) != self.bg) or \
            (logic_br is not None and self.scene.get_color(*logic_br) != self.bg)

    def hit_floor(self, rect=None):
        rect = self.rect.copy() if rect is None else rect

        logic_bl = self.scene.logic_loc((rect.left, rect.bottom), strict=True)
        logic_br = self.scene.logic_loc((rect.right - 1, rect.bottom), strict=True)

        return rect.bottom >= ScreenHeight or (logic_bl is not None and self.scene.get_color(*logic_bl) != self.bg) or \
            (self.scene.get_color(*logic_br) != self.bg)

    def hit_ceil(self, rect=None):
        rect = self.rect.copy() if rect is None else rect

        logic_tl = self.scene.logic_loc((rect.left, rect.top), strict=True)
        logic_tr = self.scene.logic_loc((rect.right - 1, rect.top), strict=True)

        return rect.bottom <= 0 or (logic_tl is not None and self.scene.get_color(*logic_tl) != self.bg) or \
            (self.scene.get_color(*logic_tr) != self.bg)


class ShiftText(ShiftElement):
    SharedImages = {}

    DefaultFontSize = 19

    def __init__(self, game, scene, text, cell_loc, bg=False, angle=0, visible=True, anchor=Anchor.center):
        super().__init__(game, scene, cell_loc, [bg, text], angle, visible, anchor)

    def set_image(self, image_attr):
        bg, text = image_attr

        self.image = get_font(self.DefaultFontSize).render(text, True, Bool2Color[not bg], Bool2Color[bg])
        self._set_rotated_image()
