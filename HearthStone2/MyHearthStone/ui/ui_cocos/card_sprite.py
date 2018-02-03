#! /usr/bin/python
# -*- coding: utf-8 -*-

"""The card sprite class."""

from cocos import actions, rect, cocosnode, euclid
from cocos.sprite import Sprite
from cocos.text import Label, HTMLLabel

from ...utils.game import Klass, Type, Rarity
from ...utils.package_io import all_cards
from ...utils.draw.cocos_utils.basic import *
from ...utils.draw.cocos_utils.active import ActiveMixin, children_inside_test
from ...utils.draw.cocos_utils.primitives import Rect

__author__ = 'fyabc'


class CardSprite(ActiveMixin, cocosnode.CocosNode):
    """The sprite of a card.
    In fact, it is a `CocosNode` that contains multiple sprites.

    The card sprite may be static (created by card_id, attributes not changed)
        or dynamic (created by card instance).
    """

    Size = euclid.Vector2(300, 450)    # Card size (original).
    SizeBase = Size // 2        # Coordinate base of children sprites.

    class _SelectEffectManager:
        def __init__(self):
            self.orig_pos = None
            self.orig_scale = None

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
            return actions.CallFuncS(_selected_fn)

        def get_unselected_eff(self):
            def _unselected_fn(spr: cocosnode.CocosNode):
                spr.scale = self.orig_scale
                spr.position = self.orig_pos
                self.orig_scale = self.orig_pos = None
            return actions.CallFuncS(_unselected_fn)

    def __init__(self, card, position=(0, 0), is_front=True, scale=1.0, **kwargs):
        super().__init__()

        self.card = card
        self.position = position
        self.scale = scale

        # For active mixin.
        self.callback = kwargs.pop('callback', self._card_clicked)
        self.callback_args = kwargs.pop('callback_args', ())
        self.callback_kwargs = kwargs.pop('callback_kwargs', {})
        self.stop_event = kwargs.pop('stop_event', True)
        self._sel_mgr = self._SelectEffectManager()
        self.selected_effect = kwargs.pop('selected_effect', self._sel_mgr.get_selected_eff())
        self.unselected_effect = kwargs.pop('unselected_effect', self._sel_mgr.get_unselected_eff())
        self.activated_effect = kwargs.pop('activated_effect', None)
        self.active_invisible = kwargs.pop('active_invisible', False)
        self.self_in_callback = kwargs.pop('self_in_callback', False)
        self.is_selected = False
        self._is_activated = False

        # Dict of front and back labels: name -> [sprite/label, z-order].
        self.front_sprites = {}
        self.back_sprites = {}
        self.activated_border = None

        self._build_components()

        self._is_front = None
        self.is_front = is_front

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, self.card)

    @property
    def static(self):
        """This is a static card (only contains card id)."""
        return isinstance(self.card, int)

    is_inside_box = children_inside_test

    def _c_get(self, key):
        """Get card attributes."""
        if self.static:
            return all_cards()[self.card].data[key]
        else:
            return getattr(self.card, key)

    def update_content(self, **kwargs):
        """Update content when the card content (not card itself) changed."""

        self.position = kwargs.pop('position', (0, 0))
        self.is_front = kwargs.pop('is_front', False)
        self.scale = kwargs.pop('scale', 1.0)

        self.front_sprites['mana-label'][0].element.text = str(self._c_get('cost'))
        if self._c_get('type') in (Type.Minion, Type.Weapon):
            self.front_sprites['attack-label'][0].element.text = str(self._c_get('attack'))
            self.front_sprites['health-label'][0].element.text = str(self._c_get('health'))
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

    def toggle_side(self):
        self.is_front = not self._is_front

    def _card_clicked(self):
        print('{} clicked!'.format(self))
        self.is_activated = not self.is_activated

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

        if self._c_get('type') == Type.Minion:
            atk_sprite = Sprite('Atk.png', pos(-0.86, -0.81, base=self.SizeBase), scale=1.15)
            atk_label = hs_style_label(str(self._c_get('attack')), pos(-0.78, -0.8, base=self.SizeBase),
                                       anchor_y='center', font_size=64)
            health_sprite = Sprite('Health.png', pos(0.84, -0.81, base=self.SizeBase), scale=1.05)
            health_label = hs_style_label(str(self._c_get('health')), pos(0.84, -0.8, base=self.SizeBase),
                                          anchor_y='center', font_size=64)
            if self._c_get('rarity') not in (Rarity.Basic, Rarity.Derivative):
                # todo: Download rarity crystals for other card types.
                self.front_sprites['rarity-sprite'] = [Sprite(
                    'Rarity-{}-{}.png'.format(0, self._c_get('rarity')), pos(0.0, -0.248, base=self.SizeBase)), 2]
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
            'font_name': kwargs.pop('font_name', DefaultFont),
            # [NOTE]: See `pyglet.text.format.html.HTMLDecoder.font_sizes` to know the font size map.
            'font_size': int(kwargs.pop('font_size', 5)),
            # Only support color names and hex colors, see in `pyglet.text.DocumentLabel`.
            'color': kwargs.pop('color', 'black'),
        }
        return '<center><font size="{font_size}" color="{color}">{desc}</font></center>'.format_map(format_map)


__all__ = [
    'CardSprite',
]
