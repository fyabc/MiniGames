#! /usr/bin/python
# -*- coding: utf-8 -*-

"""Sprites used for collection scene."""

from cocos import cocosnode, euclid, rect
from cocos.sprite import Sprite

from .select_effect import SelectEffectManager
from .utils.active import ActiveMixin, children_inside_test, ActiveSprite, ActiveGroup
from .utils.basic import hs_style_label, pos, Colors
from .utils.primitives import Rect
from ...utils.game import Rarity
from ...utils.package_io import all_cards

__author__ = 'fyabc'


class StaticCardSprite(ActiveSprite):
    """Static card sprite shown in collection scene."""

    Size = euclid.Vector2(286, 395)  # Item size (original).
    SizeBase = Size // 2  # Coordinate base of children sprites.

    def __init__(self, card_id, *args, **kwargs):
        card_image_name = all_cards()[card_id].get_image_name()

        sel_mgr_kwargs = kwargs.pop('sel_mgr_kwargs', {})

        super().__init__(card_image_name, *args, **kwargs)

        # For active mixin.
        self.sel_mgr = SelectEffectManager(self, **sel_mgr_kwargs)


class CardItem(ActiveMixin, cocosnode.CocosNode):
    """Card item sprite shown in decks."""

    Size = euclid.Vector2(200, 50)  # Item size (original).
    SizeBase = Size // 2    # Coordinate base of children sprites.

    def __init__(self, card_id, n=1, position=(0, 0), scale=1.0, **kwargs):
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


class CostFilterSprite(ActiveGroup):
    Size = euclid.Vector2(50, 50)  # Item size (original).
    SizeBase = Size // 2  # Coordinate base of children sprites.

    def __init__(self, text, filter_fn, collection_scene, position=(0, 0), scale=1.0):
        self._is_activated = None
        self.mana_sprite = None
        self.cost_label = None
        self.activated_border = None
        self.text = text

        super().__init__(
            callback=self._callback,
        )

        self.position = position
        self.scale = scale

        self.filter_fn = filter_fn
        self.collection_scene = collection_scene

        self.is_activated = False

    @property
    def is_activated(self):
        return self._is_activated

    @is_activated.setter
    def is_activated(self, value):
        if value == self._is_activated:
            return
        self._is_activated = value
        if value:
            self.activated_border.visible = True
            self.collection_scene.cost_filter_fns.add(self.filter_fn)
        else:
            self.activated_border.visible = False
            self.collection_scene.cost_filter_fns.discard(self.filter_fn)

    def _callback(self):
        # from .utils.basic import popup_input
        if not self.is_activated:
            for sprite in self.collection_scene.cost_filter_list:
                sprite.is_activated = False
            # Activate this, deactivate all others.
            self.is_activated = True
        else:
            # Just deactivate this.
            self.is_activated = False
        self.collection_scene.refresh_pages()
        # print(repr(popup_input('Hello')))

    def _build_components(self):
        self.mana_sprite = Sprite('Mana.png', pos(0.0, 0.0, base=self.SizeBase), scale=0.4)
        self.add(self.mana_sprite, z=0)

        self.cost_label = hs_style_label(
            self.text, pos(0.0, 0.0, base=self.SizeBase), anchor_x='center', anchor_y='center', font_size=20, )
        self.add(self.cost_label, z=1)

        border_rect = rect.Rect(0, 0, self.Size[0], self.Size[1])
        border_rect.center = (0, 0)
        self.activated_border = Rect(border_rect, Colors['orange'], width=2)
        self.add(self.activated_border, z=2)


__all__ = [
    'StaticCardSprite',
    'CardItem',
    'CostFilterSprite',
]
