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

    @staticmethod
    def str2anchor(anchor_name):
        """Change anchor name string to anchor value string.

        Example: 'left' -> Anchor.left ('midleft')
        """

        if anchor_name not in Anchor.LocationMap:
            return eval('Anchor.' + anchor_name)
        return anchor_name
