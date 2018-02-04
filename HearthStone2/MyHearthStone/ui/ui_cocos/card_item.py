#! /usr/bin/python
# -*- coding: utf-8 -*-

from cocos import cocosnode, euclid
from cocos.sprite import Sprite

from ...utils.package_io import all_cards
from ...utils.game import Rarity
from ...utils.draw.cocos_utils.basic import hs_style_label, pos
from ...utils.draw.cocos_utils.active import ActiveMixin, children_inside_test

__author__ = 'fyabc'


class CardItem(ActiveMixin, cocosnode.CocosNode):
    Size = euclid.Vector2(200, 50)  # Item size (original).
    SizeBase = Size // 2    # Coordinate base of children sprites.

    def __init__(self, card_id, n=1, position=(0, 0), scale=1.0, **kwargs):
        # For active mixin.
        kwargs.setdefault('stop_event', True)

        super().__init__(**kwargs)

        self.card_id = card_id
        self._n = n
        self.position = position
        self.scale = scale

        self.label_legend_star = None
        self.label_n = None
        self._build_components()

    def __repr__(self):
        return '{}(id={}, n={})'.format(self.__class__.__name__, self.card_id, self.n)

    get_box = None
    is_inside_box = children_inside_test

    @property
    def n(self):
        return self._n

    @n.setter
    def n(self, n):
        if self._n == n:
            return
        self.label_n.element.text = str(n)

        is_legend = all_cards()[self.card_id].data['rarity'] == Rarity.Legend
        if n > 1 and self._n == 1:
            self.add(self.label_n, z=1, name='label_n')
            if is_legend:
                self.remove('label_legend_star')
        elif n == 1 and self._n > 1:
            self.remove('label_n')
            if is_legend:
                self.add(self.label_legend_star, z=1, name='label_legend_star')
        self._n = n

    def get_card(self):
        return all_cards()[self.card_id]

    def _build_components(self):
        card = all_cards()[self.card_id]

        self.add(Sprite(
            'Mana.png', pos(-0.9, -0.05, base=self.SizeBase), scale=0.34,
        ), z=0, name='sprite_mana')
        self.add(hs_style_label(
            str(card.data['cost']), pos(-0.88, 0.12, base=self.SizeBase), anchor_y='center', font_size=26,
        ), z=1, name='label_mana')

        name_str = card.data['name']
        self.add(hs_style_label(
            name_str if len(name_str) <= 5 else name_str[:4] + '...',   # Shortened name
            pos(0.0, 0.0, base=self.SizeBase), anchor_y='center', font_size=20,
        ), z=0, name='label_name')

        if card.data['rarity'] == Rarity.Legend:
            self.label_legend_star = hs_style_label(
                '★', pos(0.95, 0.07, base=self.SizeBase), anchor_y='center', font_size=22, )
            if self._n == 1:
                self.add(self.label_legend_star, z=1, name='label_legend_star')
        self.label_n = hs_style_label(
            str(self._n), pos(0.95, 0.12, base=self.SizeBase), anchor_y='center', font_size=26, )
        if self._n > 1:
            self.add(self.label_n, z=1, name='label_n')


__all__ = [
    'CardItem',
]
