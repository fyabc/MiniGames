#! /usr/bin/python
# -*- coding: utf-8 -*-

from cocos.cocosnode import CocosNode
from cocos.sprite import Sprite
from cocos.text import Label, HTMLLabel
from cocos.euclid import Vector2
from pyglet import resource

from ...utils.game import Klass, Type
from ...utils.draw.constants import Colors
from ...utils.draw.cocos_utils.basic import pos, get_sprite_box, get_label_box, DefaultFont, hs_style_label
from ...utils.draw.cocos_utils.active import ActiveMixin

__author__ = 'fyabc'


class CardSprite(ActiveMixin, CocosNode):
    """The sprite of a card.

    In fact, it is a `CocosNode` that contains multiple sprites.
    """

    # TODO: change the image 'Health-8.png' into 'Health.png' + label '8', etc.
    # mana done.

    Size = Vector2(300, 450)    # Card size (original).
    SizeBase = Size // 2        # Coordinate base of children sprites.

    def __init__(self, card, position=(0, 0), is_front=True, scale=1.0, **kwargs):
        super().__init__()

        self.card = card
        self.position = position
        self.scale = scale

        # Cache for card data, for update.
        self._card_cache = dict(card.data)

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
        main_sprite = self._build_main_spr()
        mana_sprite, mana_label = self._build_mana()
        name_label = Label(card.name, position=pos(0, -0.08, base=self.SizeBase), font_size=21, anchor_x='center',
                           anchor_y='center', bold=True)
        desc_label = HTMLLabel(self._render_desc(card.description, color='black', font_size=5),
                               position=pos(0, -0.58, base=self.SizeBase), anchor_x='center', anchor_y='center',
                               width=main_sprite.width * 0.9, multiline=True)
        back_sprite = Sprite('Card_back-Classic.png', position=(0, 0), scale=1.0,)
        self.front_sprites = {
            'main': [main_sprite, 0],
            'mana-sprite': [mana_sprite, 1],
            'name': [name_label, 1],
            'desc': [desc_label, 1],
        }
        if mana_label is not None:
            self.front_sprites['mana-label'] = [mana_label, 2]
        self.back_sprites = {
            'back': [back_sprite, 0],
        }

        if card.type == Type.Minion:
            atk_sprite = Sprite('Atk-{}.png'.format(card.attack), position=pos(-0.85, -0.86, base=self.SizeBase),
                                scale=1.08)
            health_sprite = Sprite('Health-{}.png'.format(card.health), position=pos(0.85, -0.86, base=self.SizeBase),
                                   scale=1.08)
            self.front_sprites.update({'attack': [atk_sprite, 1], 'health': [health_sprite, 1]})
        elif card.type == Type.Spell:
            name_label.position = pos(0, -0.04, base=self.SizeBase)
            main_sprite.position = pos(0, -0.07, base=self.SizeBase)
        elif card.type == Type.Weapon:
            name_label.position = pos(0, -0.01, base=self.SizeBase)
            main_sprite.position = pos(0, -0.01, base=self.SizeBase)
            atk_sprite = Sprite('WeaponAtk-{}.png'.format(card.attack), position=pos(-0.85, -0.86, base=self.SizeBase),
                                scale=1.08)
            health_sprite = Sprite('WeaponHealth-{}.png'.format(card.health),
                                   position=pos(0.85, -0.86, base=self.SizeBase), scale=1.08)
            self.front_sprites.update({'attack': [atk_sprite, 1], 'health': [health_sprite, 1]})
        elif card.type == Type.HeroCard:
            armor_sprite = Sprite('HeroArmor-{}.png'.format(card.armor), position=pos(0.85, -0.86, base=self.SizeBase),
                                  scale=1.08)
            self.front_sprites.update({'armor': [armor_sprite, 1]})

        self._is_front = None
        self.is_front = is_front

    def is_inside_box(self, x, y):
        for child in self.get_children():
            if isinstance(child, Label):
                if get_label_box(child).contains(x, y):
                    return True
            elif isinstance(child, Sprite):
                if get_sprite_box(child).contains(x, y):
                    return True
        return False

    def update_content(self, **kwargs):
        """Update content when the card content (not card itself) changed."""

        self.position = kwargs.pop('position', (0, 0))
        self.is_front = kwargs.pop('is_front', False)
        self.scale = kwargs.pop('scale', 1.0)

        if self._card_cache['CAH'][0] != self.card.cost:
            # Replace image or replace sprite?
            self.front_sprites['mana-label'][0].element.text = str(self.card.cost)
        if self.card.type in (Type.Minion, Type.Weapon):
            if self._card_cache['CAH'][1] != self.card.attack:
                self.front_sprites['attack'][0].image = resource.image(self._get_image_name('attack'))
            if self._card_cache['CAH'][2] != self.card.health:
                self.front_sprites['health'][0].image = resource.image(self._get_image_name('health'))
        elif self.card.type == Type.HeroCard:
            if self._card_cache['CAH'][2] == self.card.armor:
                self.front_sprites['armor'][0].image = resource.image(self._get_image_name('armor'))
        # TODO: update components according to the cache

        self._card_cache.update(self.card.data)

    @property
    def is_front(self):
        return self._is_front

    @is_front.setter
    def is_front(self, is_front: bool):
        """Set the card side (front or back)."""
        if is_front == self.is_front:
            return

        self._is_front = is_front
        if self._is_front:
            to_be_removed = self.back_sprites
            to_be_added = self.front_sprites
        else:
            to_be_removed = self.front_sprites
            to_be_added = self.back_sprites

        for sprite, _ in to_be_removed.values():
            if sprite in self:
                self.remove(sprite)
        for sprite, z in to_be_added.values():
            self.add(sprite, z=z)

    def toggle_side(self):
        self.is_front = not self._is_front

    def _card_clicked(self):
        print('Sprite of {} clicked!'.format(self.card))

    # Internal methods to build components.
    def _get_image_name(self, name):
        """Get image name of given component."""
        if name == 'main':
            return '{}-{}.png'.format(Klass.Idx2Str[self.card.klass], self.card.type)
        elif name == 'mana-sprite':
            return 'Mana.png'
        elif name == 'back':
            return 'Card_back-Classic.png'
        elif name == 'attack':
            if self.card.type == Type.Minion:
                return 'Atk-{}.png'.format(self.card.attack)
            if self.card.type == Type.Weapon:
                return 'WeaponAtk-{}.png'.format(self.card.attack)
        elif name == 'health':
            if self.card.type == Type.Minion:
                return 'Health-{}.png'.format(self.card.health)
            if self.card.type == Type.Weapon:
                return 'WeaponHealth-{}.png'.format(self.card.health)
        elif name == 'armor':
            return 'HeroArmor-{}.png'.format(self.card.armor)
        else:
            raise ValueError('Unknown image name {!r}'.format(name))

    def _build_spr(self, name):
        pass

    def _build_main_spr(self):
        return Sprite('{}-{}.png'.format(Klass.Idx2Str[self.card.klass], self.card.type), position=(0, 0), scale=1.0,)

    def _build_mana(self):
        mana_sprite = Sprite('Mana.png', position=pos(-0.85, 0.76, base=self.SizeBase), scale=0.9,)
        if self.card.type == Type.Permanent:
            mana_label = None
        else:
            mana_label = hs_style_label(str(self.card.cost), position=pos(-0.83, 0.8, base=self.SizeBase),
                                        font_size=60, anchor_y='center', color=Colors['white'])
        return mana_sprite, mana_label

    @staticmethod
    def _render_desc(desc: str, **kwargs) -> str:
        format_map = {
            'desc': desc,
            # [NOTE]: There is an encoding bug when parsing the font name in HTML (in `pyglet\font\win32query.py:311`),
            # must set font out of HTML.
            'font_name': kwargs.pop('font_name', DefaultFont),
            # [NOTE]: See `pyglet.text.format.html.HTMLDecoder.font_sizes` to know the font size map.
            'font_size': int(kwargs.pop('font_size', 16)),
            # Only support color names and hex colors, see in `pyglet.text.DocumentLabel`.
            'color': kwargs.pop('color', 'black'),
        }
        return '<center><font size="{font_size}" color="{color}">{desc}</font></center>'.format_map(format_map)


__all__ = [
    'CardSprite',
]
