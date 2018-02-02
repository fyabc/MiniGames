#! /usr/bin/python
# -*- coding: utf-8 -*-

from cocos import cocosnode

from ...utils.draw.cocos_utils.active import ActiveMixin

__author__ = 'fyabc'


class CardItem(ActiveMixin, cocosnode.CocosNode):
    def __init__(self, card_id, n=1, position=(0, 0), scale=1.0, **kwargs):
        super().__init__()

        self.card_id = card_id
        self.n = n
        self.position = position
        self.scale = scale

        # For active mixin.
        self.callback = kwargs.pop('callback', None)
        self.callback_args = kwargs.pop('callback_args', ())
        self.callback_kwargs = kwargs.pop('callback_kwargs', {})
        self.stop_event = kwargs.pop('stop_event', True)
        self.selected_effect = kwargs.pop('selected_effect', None)
        self.unselected_effect = kwargs.pop('unselected_effect', None)
        self.activated_effect = kwargs.pop('activated_effect', None)
        self.active_invisible = kwargs.pop('active_invisible', False)
        self.self_in_callback = kwargs.pop('self_in_callback', False)
        self.is_selected = False


__all__ = [
    'CardItem',
]
