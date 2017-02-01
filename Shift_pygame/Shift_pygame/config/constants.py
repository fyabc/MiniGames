#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'fyabc'


class Anchor:
    """Enumeration of anchor. Map to names of `pygame.Rect`."""

    center = 'center'

    bottom = 'midbottom'
    top = 'midtop'
    left = 'midleft'
    right = 'midright'

    top_left = 'topleft'
    top_right = 'topright'
    bottom_left = 'bottomleft'
    bottom_right = 'bottomright'

    LocationMap = {
        center:         (0.5, 0.5),
        bottom:         (0.5, 1),
        top:            (0.5, 0),
        left:           (0, 0.5),
        right:          (1, 0.5),
        top_left:       (0, 0),
        top_right:      (1, 0),
        bottom_left:    (0, 1),
        bottom_right:   (1, 1),
    }

    _RotateChain = [
        [center],
        [bottom, left, top, right],
        [top_left, top_right, bottom_right, bottom_left],
    ]

    @staticmethod
    def str2anchor(anchor_name):
        """Change anchor name string to anchor value string.

        Example: 'left' -> Anchor.left ('midleft')
        """

        if anchor_name not in Anchor.LocationMap:
            return eval('Anchor.' + anchor_name)
        return anchor_name

    @classmethod
    def rotate(cls, anchor, angle):
        """Rotate the anchor with the angle, return a new anchor.

        :param anchor: The original anchor.
        :param angle: The angle to rotate (clockwise)
        :return: The rotated anchor.
        """

        rotate_num = angle // 90

        if anchor == cls.center:
            return anchor

        r1, r2 = cls._RotateChain[1], cls._RotateChain[2]

        if anchor in r1:
            return r1[(rotate_num + r1.index(anchor)) % 4]

        if anchor in r2:
            return r2[(rotate_num + r2.index(anchor)) % 4]

        return anchor


# Constants for the hero.

HorizontalSpeed = 0.118

# [NOTE]:
# These speeds have been set carefully.
# Do NOT change it unless you have test it many times.
InitJumpSpeed = -0.24
MaxDownSpeed = +0.2
G = +0.027  # gravity
