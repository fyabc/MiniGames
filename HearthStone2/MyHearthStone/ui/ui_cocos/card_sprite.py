#! /usr/bin/python
# -*- coding: utf-8 -*-

from .basic_components import ActiveSprite

__author__ = 'fyabc'


class CardSprite(ActiveSprite):
    """The active sprite of a card."""

    def update_content(self):
        """Update the card sprite content, called by the `update_content` method of parent layer.

        :return:
        """

        pass


__all__ = [
    'CardSprite',
]
