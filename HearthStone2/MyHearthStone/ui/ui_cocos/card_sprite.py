#! /usr/bin/python
# -*- coding: utf-8 -*-

from cocos.cocosnode import CocosNode
from cocos.sprite import Sprite

from .basic_components import ActiveMixin
from .utils import get_sprite_box

__author__ = 'fyabc'


class CardSprite(ActiveMixin, CocosNode):
    """The sprite of a card.

    In fact, it is a `CocosNode` that contains multiple sprites.
    """

    def __init__(self, card, position=(0, 0), is_front=True, scale=1.0, **kwargs):
        super().__init__()

        self.card = card
        self.position = position
        self.scale = scale

        # For active mixin.
        self.callback = kwargs.pop('callback', self._card_clicked)
        self.callback_args = kwargs.pop('callback_args', ())
        self.callback_kwargs = kwargs.pop('callback_kwargs', {})
        self.stop_event = kwargs.pop('stop_event', False)
        self.selected_effect = kwargs.pop('selected_effect', None)
        self.unselected_effect = kwargs.pop('unselected_effect', None)
        self.activated_effect = kwargs.pop('activated_effect', None)
        self.active_invisible = kwargs.pop('active_invisible', False)
        self.self_in_callback = kwargs.pop('self_in_callback', False)
        self.is_selected = False

        self.front_sprites = []
        self.back_sprites = [
            Sprite('Card_back-Classic.png', position=(0, 0), scale=1.0,),
        ]
        self._is_front = None

        # TODO: add component sprites.

        self.is_front = is_front

    def is_inside_box(self, x, y):
        for child in self.get_children():
            if get_sprite_box(child).contains(x, y):
                return True
        return False

    def update_content(self):
        """Update the card sprite content, called by the `update_content` method of parent layer.

        :return:
        """

        pass

    @property
    def is_front(self):
        return self._is_front

    @is_front.setter
    def is_front(self, is_front: bool):
        """Set the card side (front or end)."""
        if is_front == self.is_front:
            return

        self._is_front = is_front
        if self.is_front:
            to_be_removed = self.back_sprites
            to_be_added = self.front_sprites
        else:
            to_be_removed = self.front_sprites
            to_be_added = self.back_sprites

        for sprite in to_be_removed:
            self.remove(sprite)
        for sprite in to_be_added:
            self.add(sprite)

    def toggle_side(self):
        self.is_front = not self._is_front

    def _card_clicked(self):
        print('${} clicked!'.format(self))


__all__ = [
    'CardSprite',
]
