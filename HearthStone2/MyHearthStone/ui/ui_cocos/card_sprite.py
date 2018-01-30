#! /usr/bin/python
# -*- coding: utf-8 -*-

from cocos.cocosnode import CocosNode
from cocos.sprite import Sprite
from cocos.euclid import Vector2

from ...utils.game import Klass, Type

from ...utils.draw.cocos_utils.basic import get_sprite_box, pos
from ...utils.draw.cocos_utils.active import ActiveMixin

__author__ = 'fyabc'


class CardSprite(ActiveMixin, CocosNode):
    """The sprite of a card.

    In fact, it is a `CocosNode` that contains multiple sprites.
    """

    Size = Vector2(300, 450)    # Card size (original).
    SizeBase = Size // 2        # Coordinate base of children sprites.

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

        # Add component sprites.
        main_sprite = Sprite('{}-{}.png'.format(Klass.Idx2Str[card.klass], card.type), position=(0, 0), scale=1.0,)
        mana_sprite = Sprite('Mana.png' if card.type == Type.Permanent else 'Mana-{}.png'.format(card.cost),
                             position=pos(-0.85, 0.76, base=self.SizeBase), scale=0.9,)
        back_sprite = Sprite('Card_back-Classic.png', position=(0, 0), scale=1.0,)
        self.front_sprites = [main_sprite, mana_sprite]
        self.back_sprites = [back_sprite]

        if card.type == Type.Minion:
            atk_sprite = Sprite('Atk-{}.png'.format(card.attack), position=pos(-0.85, -0.86, base=self.SizeBase),
                                scale=1.08)
            health_sprite = Sprite('Health-{}.png'.format(card.health), position=pos(0.85, -0.86, base=self.SizeBase),
                                   scale=1.08)
            self.front_sprites.extend([atk_sprite, health_sprite])
        elif card.type == Type.Spell:
            main_sprite.position = pos(0.0, -0.07, base=self.SizeBase)
        elif card.type == Type.Weapon:
            main_sprite.position = pos(0.0, -0.01, base=self.SizeBase)
            atk_sprite = Sprite('WeaponAtk-{}.png'.format(card.attack), position=pos(-0.85, -0.86, base=self.SizeBase),
                                scale=1.08)
            health_sprite = Sprite('WeaponHealth-{}.png'.format(card.health),
                                   position=pos(0.85, -0.86, base=self.SizeBase), scale=1.08)
            self.front_sprites.extend([atk_sprite, health_sprite])
        elif card.type == Type.HeroCard:
            armor_sprite = Sprite('HeroArmor-{}.png'.format(card.armor), position=pos(0.85, -0.86, base=self.SizeBase),
                                  scale=1.08)
            self.front_sprites.extend([armor_sprite])

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
        if self._is_front:
            to_be_removed = self.back_sprites
            to_be_added = self.front_sprites
        else:
            to_be_removed = self.front_sprites
            to_be_added = self.back_sprites

        for sprite in to_be_removed:
            if sprite in self:
                self.remove(sprite)
        for sprite in to_be_added:
            self.add(sprite)

    def toggle_side(self):
        self.is_front = not self._is_front

    def _card_clicked(self):
        print('${} clicked!'.format(self.card))


__all__ = [
    'CardSprite',
]
