#! /usr/bin/python
# -*- coding: utf-8 -*-

"""The card sprite class."""

from cocos import rect, cocosnode, euclid
from cocos.sprite import Sprite
from cocos.text import Label, HTMLLabel
from pyglet.resource import ResourceNotFoundException, image as pyglet_image

from .select_effect import SelectEffectManager
from ...utils.constants import C
from ...utils.game import Klass, Type, Rarity
from ...utils.package_io import all_cards
from ...utils.draw.cocos_utils.basic import *
from ...utils.draw.cocos_utils.active import ActiveMixin, children_inside_test
from ...utils.draw.cocos_utils.primitives import Rect

__author__ = 'fyabc'


class EntitySprite(ActiveMixin, cocosnode.CocosNode):
    """ABC for entity sprites.

    In fact, it is a `CocosNode` that contains multiple sprites.
    """

    ActivatedColor = Colors['orange']

    def __init__(self, entity, position=(0, 0), scale=1.0, **kwargs):
        # For active mixin.
        kwargs.setdefault('callback', self._on_click)

        super().__init__(**kwargs)

        self.entity = entity
        self.position = position
        self.scale = scale

        self.activated_border = None
        self._is_activated = False

        self._build_components()

    get_box = None
    is_inside_box = children_inside_test

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, self.entity)

    @property
    def is_activated(self):
        return self._is_activated

    @is_activated.setter
    def is_activated(self, is_activated: bool):
        if self._is_activated == is_activated:
            return
        self._is_activated = is_activated
        if is_activated:
            self.add(self.activated_border, z=10)
        else:
            self.remove(self.activated_border)

    def _on_click(self):
        print('{} clicked!'.format(self))
        self.is_activated = not self.is_activated
        return True

    def _build_components(self):
        raise NotImplementedError()

    def update_content(self, **kwargs):
        """Update content when the entity content (not entity itself) changed."""
        self.position = kwargs.pop('position', (0, 0))
        self.scale = kwargs.pop('scale', 1.0)

    def _get_health_color(self):
        _h = self.entity.health
        _h_m = self.entity.max_health
        _h_s = self.entity.data['health']
        if _h < _h_m:
            return Colors['red']
        if _h_m > _h_s:
            return Colors['green']
        return Colors['white']


class HandSprite(EntitySprite):
    """The sprite of a card.

    The card sprite may be static (created by card_id, attributes not changed)
        or dynamic (created by card instance).
    """

    Size = euclid.Vector2(300, 450)    # Card size (original).
    SizeBase = Size // 2        # Coordinate base of children sprites.

    def __init__(self, card, position=(0, 0), is_front=True, scale=1.0, **kwargs):
        """todo: Add doc here.

        :param card:
        :param position:
        :type position: tuple
        :param is_front:
        :type is_front: bool
        :param scale:
        :type scale: float
        :param kwargs:
        """

        sel_mgr_kwargs = kwargs.pop('sel_mgr_kwargs', {})

        # Dict of front and back labels: name -> [sprite/label, z-order].
        self.front_sprites = {}
        self.back_sprites = {}

        super().__init__(card, position, scale, **kwargs)

        # For active mixin.
        self.sel_mgr = SelectEffectManager(self, **sel_mgr_kwargs)

        self._is_front = None
        self.is_front = is_front

    @property
    def static(self):
        """This is a static card (only contains card id)."""
        return isinstance(self.entity, (int, str))

    def _c_get(self, key):
        """Get card attributes."""
        if self.static:
            return all_cards()[self.entity].data[key]
        else:
            return getattr(self.entity, key)

    def update_content(self, **kwargs):
        super().update_content(**kwargs)
        self.is_front = kwargs.pop('is_front', False)

        # Set selected and unselected effects.
        self.sel_mgr.update_kwargs(kwargs.pop('sel_mgr_kwargs', {}))
        _sentinel = object()
        sel_eff = kwargs.pop('selected_effect', _sentinel)
        if sel_eff != _sentinel:
            self.selected_effect = sel_eff
        unsel_eff = kwargs.pop('unselected_effect', _sentinel)
        if unsel_eff != _sentinel:
            self.unselected_effect = unsel_eff
        self.sel_mgr.set_sel_eff()

        self.front_sprites['mana-label'][0].element.text = str(self._c_get('cost'))
        if self._c_get('type') in (Type.Minion, Type.Weapon):
            self.front_sprites['attack-label'][0].element.text = str(self._c_get('attack'))
            self.front_sprites['health-label'][0].element.text = str(self._c_get('health'))
            self.front_sprites['health-label'][0].element.color = self._get_health_color()
        elif self._c_get('type') == Type.HeroCard:
            self.front_sprites['armor-label'][0].element.text = str(self._c_get('armor'))
        self.front_sprites['name'][0].element.text = self._c_get('name')
        _r_desc = self._render_desc(self._c_get('description'))
        if self.front_sprites['desc'][0].element.text != _r_desc:
            self.front_sprites['desc'][0].element.text = _r_desc

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

    def _build_components(self):
        border_rect = rect.Rect(0, 0, self.Size[0], self.Size[1])
        border_rect.center = (0, 0)
        self.activated_border = Rect(border_rect, self.ActivatedColor, width=4)

        main_sprite = Sprite('{}-{}.png'.format(Klass.Idx2Str[self._c_get('klass')], self._c_get('type')), (0, 0),
                             scale=1.0,)
        try:
            if self.static:
                card_cls = all_cards()[self.entity]
            else:
                card_cls = self.entity
            image_sprite = Sprite(card_cls.get_image_name(), pos(0.0, 0.02, base=self.SizeBase), scale=1.2,)
        except ResourceNotFoundException:
            image_sprite = None

        mana_sprite = Sprite('Mana.png', pos(-0.85, 0.76, base=self.SizeBase), scale=0.9,)
        try:
            mark_sprite = Sprite('Mark-{}.png'.format(self._c_get('package')),
                                 pos(0, -0.6, base=self.SizeBase), scale=1.0)
        except ResourceNotFoundException:
            mark_sprite = None
        name_label = Label(self._c_get('name'), pos(0, -0.08, base=self.SizeBase), font_size=21, anchor_x='center',
                           anchor_y='center', bold=True)
        desc_label = HTMLLabel(self._render_desc(self._c_get('description')),
                               pos(0, -0.58, base=self.SizeBase), anchor_x='center', anchor_y='center',
                               width=main_sprite.width * 0.9, multiline=True)
        # [NOTE]: There is an encoding bug when parsing the font name in HTML (in `pyglet\font\win32query.py:311`),
        # must set font out of HTML.
        desc_label.element.set_style('font_name', C.UI.Cocos.Fonts.Description.Name)

        self.front_sprites.update({
            'main': [main_sprite, 1],
            'mana-sprite': [mana_sprite, 2],
            'name': [name_label, 3],
            'desc': [desc_label, 3],
        })
        if image_sprite is not None:
            self.front_sprites['image'] = [image_sprite, 0]
        if mark_sprite is not None:
            self.front_sprites['mark-sprite'] = [mark_sprite, 2]
        if self._c_get('type') != Type.Permanent:
            mana_label = hs_style_label(str(self._c_get('cost')), pos(-0.84, 0.8, base=self.SizeBase),
                                        font_size=64, anchor_y='center', color=Colors['white'])
            self.front_sprites['mana-label'] = [mana_label, 4]

        back_sprite = Sprite('Card_back-Classic.png', (0, 0), scale=1.0, )
        self.back_sprites['back'] = [back_sprite, 1]

        if self._c_get('rarity') not in (Rarity.Basic, Rarity.Derivative):
            self.front_sprites['rarity-sprite'] = [Sprite(
                'Rarity-{}-{}.png'.format(self._c_get('type'), self._c_get('rarity')),
                pos(0.0, -0.248, base=self.SizeBase)), 4]

        if self._c_get('type') == Type.Minion:
            atk_sprite = Sprite('Atk.png', pos(-0.86, -0.81, base=self.SizeBase), scale=1.15)
            atk_label = hs_style_label(str(self._c_get('attack')), pos(-0.78, -0.8, base=self.SizeBase),
                                       anchor_y='center', font_size=64)
            health_sprite = Sprite('Health.png', pos(0.84, -0.81, base=self.SizeBase), scale=1.05)
            health_label = hs_style_label(str(self._c_get('health')), pos(0.84, -0.8, base=self.SizeBase),
                                          anchor_y='center', font_size=64, color=self._get_health_color())
            self.front_sprites.update({
                'attack-sprite': [atk_sprite, 2],
                'attack-label': [atk_label, 3],
                'health-sprite': [health_sprite, 2],
                'health-label': [health_label, 3],
            })
        elif self._c_get('type') == Type.Spell:
            name_label.position = pos(0, -0.04, base=self.SizeBase)
            main_sprite.position = pos(0, -0.07, base=self.SizeBase)
            if mark_sprite is not None:
                mark_sprite.position = pos(0, -0.57, base=self.SizeBase)
        elif self._c_get('type') == Type.Weapon:
            name_label.position = pos(0, -0.01, base=self.SizeBase)
            main_sprite.position = pos(0, -0.01, base=self.SizeBase)
            if mark_sprite is not None:
                mark_sprite.position = pos(0, -0.55, base=self.SizeBase)
            atk_sprite = Sprite('WeaponAtk.png', pos(-0.81, -0.83, base=self.SizeBase),
                                scale=0.85)
            atk_label = hs_style_label(str(self._c_get('attack')), pos(-0.78, -0.8, base=self.SizeBase),
                                       anchor_y='center', font_size=64)
            health_sprite = Sprite('WeaponHealth.png', pos(0.82, -0.83, base=self.SizeBase), scale=0.85)
            health_label = hs_style_label(str(self._c_get('health')), pos(0.83, -0.8, base=self.SizeBase),
                                          anchor_y='center', font_size=64)
            desc_label.element.color = Colors['white']
            self.front_sprites.update({
                'attack-sprite': [atk_sprite, 2],
                'attack-label': [atk_label, 3],
                'health-sprite': [health_sprite, 2],
                'health-label': [health_label, 3],
            })
        elif self._c_get('type') == Type.HeroCard:
            armor_sprite = Sprite('HeroArmor.png', pos(0.85, -0.86, base=self.SizeBase), scale=1.08)
            armor_label = hs_style_label(str(self._c_get('armor')), pos(0.85, -0.86, base=self.SizeBase),
                                         anchor_y='center', font_size=64)
            self.front_sprites.update({
                'armor-sprite': [armor_sprite, 2],
                'armor-label': [armor_label, 3],
            })

    @staticmethod
    def _render_desc(desc: str, **kwargs) -> str:
        format_map = {
            'desc': desc,
            # [NOTE]: See `pyglet.text.format.html.HTMLDecoder.font_sizes` to know the font size map.
            'font_size': int(kwargs.pop('font_size', 5)),
            # Only support color names and hex colors, see in `pyglet.text.DocumentLabel`.
            'color': kwargs.pop('color', 'black'),
        }
        return '<center><font size="{font_size}" color="{color}">{desc}</font></center>'.format_map(format_map)

    def _get_health_color(self):
        if self.static:
            return Colors['white']
        return super()._get_health_color()


class MinionSprite(EntitySprite):
    ImagePart = 0.40, 0.38
    ImageScale = 0.9

    ImageSize = euclid.Vector2(286, 395)    # Card size (original).
    Size = euclid.Vector2(                  # Sprite size.
        int(ImageSize[0] * ImagePart[0] * ImageScale), int(ImageSize[1] * ImagePart[1] * ImageScale))
    SizeBase = Size // 2  # Coordinate base of children sprites.

    CommonColor = Colors['gray30']

    def __init__(self, minion, position=(0, 0), scale=1.0, **kwargs):
        super().__init__(minion, position, scale, **kwargs)

        # Show enchantments of this minion.
        self.enchantments = []

        # TODO: Show the related card when mouse on it over N seconds.
        self.related_card = None

    def _build_components(self):
        border_rect = rect.Rect(0, 0, self.Size[0], self.Size[1])
        border_rect.center = (0, 0)
        self.activated_border = Rect(border_rect, self.ActivatedColor, width=4)

        self.common_border = Rect(border_rect, self.CommonColor, width=2)
        self.add(self.common_border, z=1)

        # Get the part of card image.
        try:
            image = pyglet_image(self.entity.get_image_name()).get_region(
                x=int(self.ImageSize[0] * (1 - self.ImagePart[0]) / 2), y=int(self.ImageSize[1] * 0.51),
                width=int(self.ImageSize[0] * self.ImagePart[0]), height=int(self.ImageSize[1] * self.ImagePart[1]))
            image_sprite = Sprite(image, pos(0.0, 0.0, base=self.SizeBase), scale=self.ImageScale,)
            self.add(image_sprite, z=0)
        except ResourceNotFoundException:
            pass

        # TODO


class HeroSprite(EntitySprite):
    """The hero sprite."""

    Size = euclid.Vector2(300, 425)  # Card size (original).
    SizeBase = Size // 2  # Coordinate base of children sprites.

    def __init__(self, hero, position=(0, 0), scale=1.0, **kwargs):
        self.attack_label = None
        self.health_label = None

        super().__init__(hero, position, scale, **kwargs)

    def _build_components(self):
        border_rect = rect.Rect(0, 0, self.Size[0], self.Size[1])
        border_rect.center = (0, 0)
        self.activated_border = Rect(border_rect, self.ActivatedColor, width=4)

        self.add(Sprite('Hero.png', pos(0, 0, base=self.SizeBase), scale=1.0))

        self.health_label = hs_style_label(str(self.entity.health), pos(0.73, -0.34, base=self.SizeBase),
                                           font_size=46, anchor_y='center', color=self._get_health_color())
        self.add(self.health_label, z=1)

    def update_content(self, **kwargs):
        super().update_content(**kwargs)
        self.health_label.element.text = str(self.entity.health)
        self.health_label.element.color = self._get_health_color()


class HeroPowerSprite(EntitySprite):
    """The hero power sprite."""

    def _build_components(self):
        pass


__all__ = [
    'EntitySprite',
    'HandSprite',
    'MinionSprite',
    'HeroSprite',
    'HeroPowerSprite',
]
