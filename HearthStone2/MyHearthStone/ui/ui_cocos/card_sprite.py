#! /usr/bin/python
# -*- coding: utf-8 -*-

"""The card sprite class."""

from cocos import actions, rect, cocosnode, euclid
from cocos.sprite import Sprite
from cocos.text import Label, HTMLLabel

from ...utils.constants import C
from ...utils.game import Klass, Type, Rarity
from ...utils.package_io import all_cards
from ...utils.draw.cocos_utils.basic import *
from ...utils.draw.cocos_utils.active import ActiveMixin, children_inside_test
from ...utils.draw.cocos_utils.primitives import Rect
from ...utils.draw.cocos_utils.node_tree import set_z

__author__ = 'fyabc'


class EntitySprite(ActiveMixin, cocosnode.CocosNode):
    """ABC for entity sprites.

    In fact, it is a `CocosNode` that contains multiple sprites.
    """

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
            self.add(self.activated_border, z=3)
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


class CardSprite(EntitySprite):
    """The sprite of a card.

    The card sprite may be static (created by card_id, attributes not changed)
        or dynamic (created by card instance).
    """

    Size = euclid.Vector2(300, 450)    # Card size (original).
    SizeBase = Size // 2        # Coordinate base of children sprites.

    class _SelectEffectManager:
        """The helper class for select and unselect effects."""
        # TODO: make this class more configurable.
        def __init__(self, move_to_top=False):
            self.orig_pos = None
            self.orig_scale = None
            self.move_to_top = move_to_top

        def get_selected_eff(self):
            def _selected_fn(spr: cocosnode.CocosNode):
                self.orig_scale = spr.scale
                self.orig_pos = spr.position

                spr.scale *= 2
                y_ratio = spr.y / get_height()
                if y_ratio < 0.5:
                    spr.y = min(y_ratio + 0.13, 0.5) * get_height()
                else:
                    spr.y = max(y_ratio - 0.13, 0.5) * get_height()

                if self.move_to_top:
                    set_z(spr, z='top')
            return actions.CallFuncS(_selected_fn)

        def get_unselected_eff(self):
            def _unselected_fn(spr: cocosnode.CocosNode):
                spr.scale = self.orig_scale
                spr.position = self.orig_pos
                self.orig_scale = self.orig_pos = None
            return actions.CallFuncS(_unselected_fn)

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
        # For active mixin.
        self.sel_mgr = self._SelectEffectManager(**kwargs.pop('sel_mgr_kwargs', {}))
        kwargs.setdefault('selected_effect', 'default')
        kwargs.setdefault('unselected_effect', 'default')

        # Dict of front and back labels: name -> [sprite/label, z-order].
        self.front_sprites = {}
        self.back_sprites = {}

        super().__init__(card, position, scale, **kwargs)

        self._set_sel_eff()
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

    def _set_sel_eff(self):
        """Set selected and unselected effects, translate string values into actions."""
        if self.selected_effect == 'default':
            self.selected_effect = self.sel_mgr.get_selected_eff()
        if self.unselected_effect == 'default':
            self.unselected_effect = self.sel_mgr.get_unselected_eff()

    def update_content(self, **kwargs):
        super().update_content(**kwargs)
        self.is_front = kwargs.pop('is_front', False)

        # Set selected and unselected effects.
        _sentinel = object()
        sel_eff = kwargs.pop('selected_effect', _sentinel)
        if sel_eff != _sentinel:
            self.selected_effect = sel_eff
        unsel_eff = kwargs.pop('unselected_effect', _sentinel)
        if unsel_eff != _sentinel:
            self.unselected_effect = unsel_eff
        self._set_sel_eff()

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
        self.activated_border = Rect(border_rect, Colors['lightgreen'], width=4)

        main_sprite = Sprite('{}-{}.png'.format(Klass.Idx2Str[self._c_get('klass')], self._c_get('type')), (0, 0),
                             scale=1.0,)
        mana_sprite = Sprite('Mana.png', pos(-0.85, 0.76, base=self.SizeBase), scale=0.9,)
        name_label = Label(self._c_get('name'), pos(0, -0.08, base=self.SizeBase), font_size=21, anchor_x='center',
                           anchor_y='center', bold=True)
        desc_label = HTMLLabel(self._render_desc(self._c_get('description')),
                               pos(0, -0.58, base=self.SizeBase), anchor_x='center', anchor_y='center',
                               width=main_sprite.width * 0.9, multiline=True)

        self.front_sprites.update({
            'main': [main_sprite, 0],
            'mana-sprite': [mana_sprite, 1],
            'name': [name_label, 1],
            'desc': [desc_label, 1],
        })
        if self._c_get('type') != Type.Permanent:
            mana_label = hs_style_label(str(self._c_get('cost')), pos(-0.84, 0.8, base=self.SizeBase),
                                        font_size=64, anchor_y='center', color=Colors['white'])
            self.front_sprites['mana-label'] = [mana_label, 2]

        back_sprite = Sprite('Card_back-Classic.png', (0, 0), scale=1.0, )
        self.back_sprites['back'] = [back_sprite, 0]

        if self._c_get('rarity') not in (Rarity.Basic, Rarity.Derivative):
            self.front_sprites['rarity-sprite'] = [Sprite(
                'Rarity-{}-{}.png'.format(self._c_get('type'), self._c_get('rarity')),
                pos(0.0, -0.248, base=self.SizeBase)), 2]

        if self._c_get('type') == Type.Minion:
            atk_sprite = Sprite('Atk.png', pos(-0.86, -0.81, base=self.SizeBase), scale=1.15)
            atk_label = hs_style_label(str(self._c_get('attack')), pos(-0.78, -0.8, base=self.SizeBase),
                                       anchor_y='center', font_size=64)
            health_sprite = Sprite('Health.png', pos(0.84, -0.81, base=self.SizeBase), scale=1.05)
            health_label = hs_style_label(str(self._c_get('health')), pos(0.84, -0.8, base=self.SizeBase),
                                          anchor_y='center', font_size=64, color=self._get_health_color())
            self.front_sprites.update({
                'attack-sprite': [atk_sprite, 1],
                'attack-label': [atk_label, 2],
                'health-sprite': [health_sprite, 1],
                'health-label': [health_label, 2],
            })
        elif self._c_get('type') == Type.Spell:
            name_label.position = pos(0, -0.04, base=self.SizeBase)
            main_sprite.position = pos(0, -0.07, base=self.SizeBase)
        elif self._c_get('type') == Type.Weapon:
            name_label.position = pos(0, -0.01, base=self.SizeBase)
            main_sprite.position = pos(0, -0.01, base=self.SizeBase)
            atk_sprite = Sprite('WeaponAtk.png', pos(-0.81, -0.83, base=self.SizeBase),
                                scale=0.85)
            atk_label = hs_style_label(str(self._c_get('attack')), pos(-0.78, -0.8, base=self.SizeBase),
                                       anchor_y='center', font_size=64)
            health_sprite = Sprite('WeaponHealth.png', pos(0.82, -0.83, base=self.SizeBase), scale=0.85)
            health_label = hs_style_label(str(self._c_get('health')), pos(0.83, -0.8, base=self.SizeBase),
                                          anchor_y='center', font_size=64)
            desc_label.element.color = Colors['white']
            self.front_sprites.update({
                'attack-sprite': [atk_sprite, 1],
                'attack-label': [atk_label, 2],
                'health-sprite': [health_sprite, 1],
                'health-label': [health_label, 2],
            })
        elif self._c_get('type') == Type.HeroCard:
            armor_sprite = Sprite('HeroArmor.png', pos(0.85, -0.86, base=self.SizeBase), scale=1.08)
            armor_label = hs_style_label(str(self._c_get('armor')), pos(0.85, -0.86, base=self.SizeBase),
                                         anchor_y='center', font_size=64)
            self.front_sprites.update({
                'armor-sprite': [armor_sprite, 1],
                'armor-label': [armor_label, 2],
            })

    @staticmethod
    def _render_desc(desc: str, **kwargs) -> str:
        format_map = {
            'desc': desc,
            # [NOTE]: There is an encoding bug when parsing the font name in HTML (in `pyglet\font\win32query.py:311`),
            # must set font out of HTML.
            'font_name': kwargs.pop('font_name', C.UI.Cocos.DefaultFont),
            # [NOTE]: See `pyglet.text.format.html.HTMLDecoder.font_sizes` to know the font size map.
            'font_size': int(kwargs.pop('font_size', 4)),
            # Only support color names and hex colors, see in `pyglet.text.DocumentLabel`.
            'color': kwargs.pop('color', 'black'),
        }
        return '<center><font size="{font_size}" color="{color}">{desc}</font></center>'.format_map(format_map)

    def _get_health_color(self):
        if self.static:
            return Colors['white']
        return super()._get_health_color()


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
        self.activated_border = Rect(border_rect, Colors['lightgreen'], width=4)

        self.add(Sprite('Hero.png', pos(0, 0, base=self.SizeBase), scale=1.0))

        self.health_label = hs_style_label(str(self.entity.health), pos(0.73, -0.34, base=self.SizeBase),
                                           font_size=46, anchor_y='center', color=self._get_health_color())
        self.add(self.health_label, z=1)

    def update_content(self, **kwargs):
        super().update_content(**kwargs)
        self.health_label.element.text = str(self.entity.health)
        self.health_label.element.color = self._get_health_color()


__all__ = [
    'EntitySprite',
    'CardSprite',
    'HeroSprite',
]
