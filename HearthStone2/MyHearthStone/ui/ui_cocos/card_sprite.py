#! /usr/bin/python
# -*- coding: utf-8 -*-

"""The card sprite class."""

from cocos import rect, cocosnode, euclid
from cocos.sprite import Sprite
from cocos.text import Label, HTMLLabel

from .select_effect import SelectEffectManager
from .utils.active import ActiveMixin, children_inside_test
from .utils.basic import *
from .utils.primitives import Rect
from ...utils.constants import C
from ...utils.game import Klass, Type, Rarity, Race
from ...utils.package_io import all_cards

__author__ = 'fyabc'


class EntitySprite(ActiveMixin, cocosnode.CocosNode):
    """ABC for entity sprites.

    In fact, it is a `CocosNode` that contains multiple sprites.
    """

    # Card action border colors.
    CommonColor = Colors['gray30']
    CanActionColor = Colors['green']
    HighlightColor = Colors['red']

    # Color when this entity is selected.
    SelectedColor = Colors['orange']

    def __init__(self, entity, position=(0, 0), scale=1.0, **kwargs):
        # For active mixin.
        kwargs.setdefault('callback', self._on_click)

        super().__init__(**kwargs)

        self.entity = entity
        self.position = position
        self.scale = scale

        # The border that indicate this sprite is activated.
        self.activated_border = None
        self._is_activated = False

        # The border that indicate the status of this sprite (inactive, active, highlighted).
        self.status_border = None

        self._build_components()

    get_box = None
    is_inside_box = children_inside_test

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, self.entity)

    def add_to_layer(self, layer, z=0, name=None):
        layer.add(self, z=z, name=name)
        self.update_status_border()

    @property
    def static(self):
        """This is a static card (only contains card id)."""
        return isinstance(self.entity, (int, str))

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
        # print('{} clicked!'.format(self))
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
        _h_s = self.entity.cls_data['health']
        if _h < _h_m:
            return Colors['red']
        if _h_m > _h_s:
            return Colors['green']
        return Colors['white']

    def _get_attack_color(self):
        _a = self.entity.attack
        _a_s = self.entity.cls_data['attack']
        if _a > _a_s:
            return Colors['green']
        return Colors['white']

    def _get_cost_color(self):
        _c = self.entity.cost
        _c_s = self.entity.cls_data['cost']
        if _c > _c_s:
            return Colors['red']
        elif _c < _c_s:
            return Colors['green']
        return Colors['white']

    def _create_status_border(self, border_rect, width, z):
        self.status_border = Rect(border_rect, self.CanActionColor, width=width)
        self.status_border.visible = False
        self.add(self.status_border, z=z)

    def in_control(self):
        if self.static:
            return False
        player_id, game = self.entity.player_id, self.entity.game
        if self.parent.hot_seat:
            return player_id == game.current_player
        else:
            return player_id == 0

    def update_status_border(self):
        if not self.in_control():
            self.status_border.visible = False
            return

        action_status = self.entity.can_do_action()
        if action_status == self.entity.Inactive:
            self.status_border.visible = False
        else:
            if action_status == self.entity.Active:
                color = self.CanActionColor
            else:  # action_status == self.entity.Highlighted
                color = self.HighlightColor
            self.status_border.color = color
            self.status_border.visible = True

    def _update_attr_sprite(self, attr_name, get_fn, z):
        if getattr(self.entity, attr_name):
            sprite = get_fn()
            self.try_add(sprite, z=z)
        else:
            sprite = get_fn()
            self.try_remove(sprite)


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

    def _c_get(self, key):
        """Get card attributes."""
        if self.static:
            card = all_cards()[self.entity]
            if key == 'description':
                return card.static_description()
            return card.data[key]
        else:
            return getattr(self.entity, key)

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

    @staticmethod
    def _render_desc(desc: str, **kwargs) -> str:
        # TODO: Reduce the font size when the description is too long.
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

    def _get_attack_color(self):
        if self.static:
            return Colors['white']
        return super()._get_attack_color()

    def _build_components(self):
        border_rect = rect.Rect(0, 0, self.Size[0], self.Size[1])
        border_rect.center = (0, 0)
        self.activated_border = Rect(border_rect, self.SelectedColor, width=4)

        if not self.static:
            self._create_status_border(border_rect, z=3, width=4)

        # Main card image.
        main_sprite = Sprite('{}-{}.png'.format(Klass.Idx2Str[self._c_get('klass')], self._c_get('type')), (0, 0),
                             scale=1.0,)
        if self.static:
            card_cls = all_cards()[self.entity]
        else:
            card_cls = self.entity
        main_image = try_load_image(card_cls.get_image_name())
        if main_image is not None:
            image_sprite = Sprite(main_image, pos(0.0, 0.02, base=self.SizeBase), scale=1.2,)
            self.front_sprites['image'] = [image_sprite, 0]

        mana_sprite = Sprite('Mana.png', pos(-0.85, 0.76, base=self.SizeBase), scale=0.9,)

        # Mark, name and description.
        mark_image = try_load_image('Mark-{}.png'.format(self._c_get('package')))
        mark_sprite = None if mark_image is None else Sprite(mark_image, pos(0, -0.6, base=self.SizeBase), scale=1.0)
        name_label = Label(self._c_get('name'), pos(0, -0.08, base=self.SizeBase), font_size=21, anchor_x='center',
                           anchor_y='center', bold=True)
        desc_label = HTMLLabel(self._render_desc(self._c_get('description')),
                               pos(0, -0.58, base=self.SizeBase), anchor_x='center', anchor_y='center',
                               width=main_sprite.width * 0.9, multiline=True)
        # [NOTE]: There is an encoding bug when parsing the font name in HTML (in `pyglet\font\win32query.py:311`),
        # must set font out of HTML.
        desc_label.element.set_style('font_name', C.UI.Cocos.Fonts.Description.Name)

        # Race sprite and label.
        race = self._c_get('race')
        if race:
            race_sprite = Sprite('Race.png', pos(0.02, -0.86, base=self.SizeBase), scale=1.0)
            race_label = hs_style_label('，'.join(Race.Idx2Str[r] for r in race), pos(0.02, -0.86, base=self.SizeBase),
                                        font_size=22, anchor_y='center')
            self.front_sprites['race-sprite'] = [race_sprite, 3]
            self.front_sprites['race-label'] = [race_label, 4]

        self.front_sprites.update({
            'main': [main_sprite, 1],
            'mana-sprite': [mana_sprite, 2],
            'name': [name_label, 3],
            'desc': [desc_label, 3],
        })
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
                                       anchor_y='center', font_size=64, color=self._get_attack_color())
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

    def update_status_border(self):
        if not self.static:
            super().update_status_border()

    def update_content(self, **kwargs):
        super().update_content(**kwargs)
        self.is_front = kwargs.pop('is_front', False)

        # Set selected and unselected effects.
        self.sel_mgr.update_kwargs(kwargs.pop('sel_mgr_kwargs', {}))
        _sentinel = object()
        sel_eff = kwargs.pop('selected_effect', _sentinel)
        if sel_eff is not _sentinel:
            self.selected_effect = sel_eff
        unsel_eff = kwargs.pop('unselected_effect', _sentinel)
        if unsel_eff is not _sentinel:
            self.unselected_effect = unsel_eff
        self.sel_mgr.set_sel_eff()

        self.front_sprites['mana-label'][0].element.text = str(self._c_get('cost'))
        self.front_sprites['mana-label'][0].element.color = self._get_cost_color()
        if self._c_get('type') in (Type.Minion, Type.Weapon):
            self.front_sprites['attack-label'][0].element.text = str(self._c_get('attack'))
            self.front_sprites['health-label'][0].element.text = str(self._c_get('health'))
            self.front_sprites['attack-label'][0].element.color = self._get_attack_color()
            self.front_sprites['health-label'][0].element.color = self._get_health_color()
        elif self._c_get('type') == Type.HeroCard:
            self.front_sprites['armor-label'][0].element.text = str(self._c_get('armor'))
        self.front_sprites['name'][0].element.text = self._c_get('name')
        _r_desc = self._render_desc(self._c_get('description'))
        _e_desc = self.front_sprites['desc'][0].element
        if _e_desc.text != _r_desc:
            _e_desc.text = _r_desc
            _e_desc.set_style('font_name', C.UI.Cocos.Fonts.Description.Name)

        # [NOTE] Race sprite and label not updated.


class MinionSprite(EntitySprite):
    ImagePart = 0.30, 0.51, 0.40, 0.38      # Start x, start y, width, height
    ImageScale = 0.9

    ImageSize = euclid.Vector2(286, 395)    # Card size (original).
    Size = euclid.Vector2(                  # Sprite size.
        int(ImageSize[0] * ImagePart[2] * ImageScale), int(ImageSize[1] * ImagePart[3] * ImageScale))
    SizeBase = Size // 2  # Coordinate base of children sprites.

    def __init__(self, minion, position=(0, 0), scale=1.0, **kwargs):
        self.image_sprite = None
        self.atk_label = None
        self.health_label = None

        # Show enchantments of this minion.
        self.enchantments = []

        # TODO: Windfury sprite, etc.
        self.divine_shield_sprite = None
        self.taunt_sprite = None
        self.frozen_sprite = None
        self.deathrattle_sprite = None
        self.trigger_sprite = None

        # TODO: Show the related card when mouse on it over N seconds.
        # TODO: (Need support of focus time in ``ActiveMixin``.)
        self.related_card = None

        super().__init__(minion, position, scale, **kwargs)

    def _get_ds_sprite(self):
        if self.divine_shield_sprite is None:
            self.divine_shield_sprite = Sprite(
                'DivineShield.png', pos(0.0, 0.0, base=self.SizeBase),
                opacity=80)
            self.divine_shield_sprite.scale_x = self.ImageScale * self.ImagePart[2] * 1.1
            self.divine_shield_sprite.scale_y = self.ImageScale * self.ImagePart[3] * 1.1
        return self.divine_shield_sprite

    def _get_taunt_sprite(self):
        if self.taunt_sprite is None:
            self.taunt_sprite = Sprite(
                'TauntMarker.png', pos(-0.05, 0.0, base=self.SizeBase),
                opacity=200,
            )
            self.taunt_sprite.scale_x = self.ImageScale * self.ImagePart[2] * 5.472222
            self.taunt_sprite.scale_y = self.ImageScale * self.ImagePart[3] * 6.140351
        return self.taunt_sprite

    def _get_frozen_sprite(self):
        if self.frozen_sprite is None:
            self.frozen_sprite = Sprite(
                'Frozen.png', pos(0.00, 0.00, base=self.SizeBase),
                scale=0.55, opacity=200,
            )
        return self.frozen_sprite

    def _get_dr_sprite(self):
        if self.deathrattle_sprite is None:
            self.deathrattle_sprite = Sprite(
                'Deathrattle.png', pos(0.00, -0.90, base=self.SizeBase),
                scale=0.7,
            )
        return self.deathrattle_sprite

    def _stealth_opacity(self):
        return 50 if self.entity.stealth else 255

    def _build_components(self):
        border_rect = rect.Rect(0, 0, self.Size[0], self.Size[1])
        border_rect.center = (0, 0)
        self.activated_border = Rect(border_rect, self.SelectedColor, width=4)

        self._create_status_border(border_rect, z=3, width=2)
        self.status_border.visible = True

        # Get the part of card image.
        image = try_load_image(self.entity.get_image_name(), image_part=self.ImagePart, default='Minion-Skeleton.png')
        self.image_sprite = Sprite(
            image, pos(0.0, 0.0, base=self.SizeBase), scale=self.ImageScale, opacity=self._stealth_opacity())
        self.add(self.image_sprite, z=2)

        if self.entity.type == Type.Minion:
            atk_sprite = Sprite('Atk.png', pos(-0.92, -0.81, base=self.SizeBase), scale=0.6)
            self.atk_label = hs_style_label(str(self.entity.attack), pos(-0.84, -0.8, base=self.SizeBase),
                                            anchor_y='center', font_size=32, color=self._get_attack_color())
            health_sprite = Sprite('Health.png', pos(0.88, -0.81, base=self.SizeBase), scale=0.56)
            self.health_label = hs_style_label(str(self.entity.health), pos(0.86, -0.8, base=self.SizeBase),
                                               anchor_y='center', font_size=32, color=self._get_health_color())
            self.add(atk_sprite, z=3)
            self.add(self.atk_label, z=4)
            self.add(health_sprite, z=3)
            self.add(self.health_label, z=4)
        else:   # self.entity.type == Type.Permanent
            pass

    def update_status_border(self):
        if not self.in_control():
            self.status_border.color = self.CommonColor
        else:
            action_status = self.entity.can_do_action()
            if action_status == self.entity.Inactive:
                color = self.CommonColor
            elif action_status == self.entity.Active:
                color = self.CanActionColor
            else:   # action_status == self.entity.Highlighted
                color = self.HighlightColor
            self.status_border.color = color

    def update_content(self, **kwargs):
        super().update_content(**kwargs)

        if self.entity.type == Type.Minion:
            if self.image_sprite is not None:
                self.image_sprite.opacity = self._stealth_opacity()
            self.atk_label.element.text = str(self.entity.attack)
            self.atk_label.element.color = self._get_attack_color()
            self.health_label.element.text = str(self.entity.health)
            self.health_label.element.color = self._get_health_color()
            self._update_attr_sprite('divine_shield', self._get_ds_sprite, z=6)

            # TODO: Set taunt opacity to 50 if this minion is negated_taunt.
            self._update_attr_sprite('taunt', self._get_taunt_sprite, z=0)

            self._update_attr_sprite('frozen', self._get_frozen_sprite, z=5)

            # TODO: Only show one sprite at mid-bottom when more than one available (show which?).
            self._update_attr_sprite('dr_list', self._get_dr_sprite, z=5)

        else:   # self.entity.type == Type.Permanent
            # Anything to do?
            pass


class HeroSprite(EntitySprite):
    """The hero sprite."""

    Size = euclid.Vector2(300, 425)  # Card size (original).
    SizeBase = Size // 2  # Coordinate base of children sprites.

    ImagePart = 0.10, 0.35, 0.76, 0.65  # Start x, start y, width, height
    ImageScale = 1.15

    def __init__(self, user, hero, position=(0, 0), scale=1.0, **kwargs):
        self.user = user

        # The border that indicate the status of this sprite (inactive, active, highlighted).
        self.attack_label = None
        self.health_label = None
        self.armor_sprite = None
        self.armor_label = None
        self.frozen_sprite = None

        super().__init__(hero, position, scale, **kwargs)

    def _get_frozen_sprite(self):
        if self.frozen_sprite is None:
            self.frozen_sprite = Sprite(
                'Frozen.png', pos(-0.00, 0.10, base=self.SizeBase),
                scale=1.0, opacity=200,
            )
        return self.frozen_sprite

    def _build_components(self):
        border_rect = rect.Rect(0, 0, self.Size[0], self.Size[1])
        border_rect.center = (0, 0)
        self.activated_border = Rect(border_rect, self.SelectedColor, width=4)
        self._create_status_border(border_rect, width=2, z=4)

        # Hero image (background and blank foreground).
        image = try_load_image('Hero-{}.png'.format(self.entity.id), image_part=self.ImagePart)
        if image is not None:
            self.add(Sprite(image, pos(0.05, 0.255, base=self.SizeBase), scale=self.ImageScale), z=0)
        self.add(Sprite('Hero.png', pos(0, 0, base=self.SizeBase), scale=1.0, opacity=255), z=1)
        self.add(hs_style_label(str(self.user.nickname), pos(0.0, -0.54, base=self.SizeBase),
                                font_size=18, anchor_y='center'), z=2)
        self.add(hs_style_label(str(self.entity.name), pos(0.0, -0.65, base=self.SizeBase),
                                font_size=12, anchor_y='center'), z=2)

        self.attack_sprite = Sprite('Atk.png', pos(-0.75, -0.34, base=self.SizeBase), scale=1.0)
        self.attack_sprite.visible = False
        self.add(self.attack_sprite, z=2)
        self.attack_label = hs_style_label('0', pos(-0.687, -0.34, base=self.SizeBase),
                                           font_size=46, anchor_y='center', color=Colors['white'])
        self.attack_label.visible = False
        self.add(self.attack_label, z=3)
        self.health_label = hs_style_label(str(self.entity.health), pos(0.73, -0.34, base=self.SizeBase),
                                           font_size=46, anchor_y='center', color=self._get_health_color())
        self.add(self.health_label, z=2)
        self.armor_sprite = Sprite('Armor.png', pos(0.71, -0.00, base=self.SizeBase), scale=1.0)
        self.armor_sprite.visible = False
        self.add(self.armor_sprite, z=2)
        self.armor_label = hs_style_label('0', pos(0.71, 0.04, base=self.SizeBase),
                                          font_size=46, anchor_y='center', color=Colors['white'])
        self.armor_label.visible = False
        self.add(self.armor_label, z=3)

    def update_content(self, **kwargs):
        super().update_content(**kwargs)

        attack = self.entity.attack
        self.attack_label.element.text = str(attack)
        self.attack_label.visible = attack > 0
        self.attack_sprite.visible = attack > 0

        self.health_label.element.text = str(self.entity.health)
        self.health_label.element.color = self._get_health_color()

        armor = self.entity.armor
        if armor == 0:
            self.armor_label.visible = False
            self.armor_sprite.visible = False
        else:
            self.armor_label.element.text = str(armor)
            self.armor_label.visible = True
            self.armor_sprite.visible = True

        self._update_attr_sprite('frozen', self._get_frozen_sprite, z=3)


class HeroPowerSprite(EntitySprite):
    """The hero power sprite."""

    Size = euclid.Vector2(100, 100)  # Hero power size (original).
    SizeBase = Size // 2  # Coordinate base of children sprites.

    ImagePart = 0.31, 0.59, 0.40, 0.25      # Start x, start y, width, height
    ImageScale = 0.6

    def __init__(self, hero_power, position=(0, 0), scale=1.0, **kwargs):
        self.common_border = None
        self.hp_available = None
        self.hp_sprite = None
        self.hp_cost_label = None
        self.hp_exhausted = None

        super().__init__(hero_power, position, scale, **kwargs)

    def _build_components(self):
        border_rect = rect.Rect(0, 0, self.Size[0], self.Size[1])
        border_rect.center = (0, 0)
        self.activated_border = Rect(border_rect, self.SelectedColor, width=4)

        # TODO: Change this into a circle?
        self._create_status_border(border_rect, width=2, z=3)

        self.hp_available = Sprite('HeroPower.png', pos(0, 0.05, base=self.SizeBase), scale=1.0)
        image = try_load_image('HeroPower-{}.png'.format(self.entity.id), image_part=self.ImagePart)
        self.hp_sprite = Sprite(image, scale=self.ImageScale)
        self.hp_cost_label = hs_style_label(str(self.entity.cost), pos(0, 0.633, base=self.SizeBase), font_size=24)
        self.hp_exhausted = Sprite('HeroPowerExhausted.png', pos(0, 0, base=self.SizeBase), scale=1.0)

    def update_content(self, **kwargs):
        super().update_content(**kwargs)

        self.hp_cost_label.element.text = str(self.entity.cost)
        self.hp_cost_label.element.color = self._get_cost_color()
        if self.entity.exhausted:
            self.try_remove(self.hp_available)
            self.try_remove(self.hp_sprite)
            self.try_remove(self.hp_cost_label)
            self.try_add(self.hp_exhausted, z=1)
        else:
            self.try_add(self.hp_available, z=2)
            self.try_add(self.hp_sprite, z=1)
            self.try_add(self.hp_cost_label, z=3)
            self.try_remove(self.hp_exhausted)


class HeroPowerFullArtSprite(EntitySprite):
    ImagePart = 0.00, 0.00, 1.00, 1.00
    ImageScale = 1.0

    ImageSize = euclid.Vector2(286, 395)  # Hero power size (original).
    Size = euclid.Vector2(  # Sprite size.
        int(ImageSize[0] * ImagePart[2] * ImageScale), int(ImageSize[1] * ImagePart[3] * ImageScale))
    SizeBase = Size // 2  # Coordinate base of children sprites.

    def __init__(self, hero_power, position=(0, 0), scale=1.0, **kwargs):
        self.hp_sprite = None
        self.hp_cost_sprite = None
        self.hp_cost_label = None

        super().__init__(hero_power, position, scale, **kwargs)

    def _build_components(self):
        image = try_load_image('HeroPower-{}.png'.format(self.entity.id), image_part=self.ImagePart)
        self.hp_sprite = Sprite(image, scale=self.ImageScale)
        self.hp_cost_sprite = Sprite('Mana.png', pos(0.00, 0.805, base=self.SizeBase), scale=0.62,)
        self.hp_cost_label = hs_style_label(str(self.entity.cost), pos(0, 0.72, base=self.SizeBase), font_size=42)

        self.add(self.hp_sprite, z=0)
        self.add(self.hp_cost_sprite, z=1)
        self.add(self.hp_cost_label, z=2)

    def update_status_border(self):
        # Full art hero power does not have status border.
        pass

    def update_content(self, **kwargs):
        super().update_content(**kwargs)
        self.hp_cost_label.element.text = str(self.entity.cost)
        self.hp_cost_label.element.color = self._get_cost_color()


class WeaponSprite(EntitySprite):
    """The weapon sprite."""

    Size = euclid.Vector2(120, 120)  # Weapon size (original).
    SizeBase = Size // 2  # Coordinate base of children sprites.

    ImagePart = 0.22, 0.50, 0.58, 0.38
    ImageScale = 0.5

    def __init__(self, weapon, position=(0, 0), scale=1.0, **kwargs):
        self.border_sprite = None
        self.main_sprite = None
        self.sheathed_sprite = None
        self.attack_sprite, self.attack_label = None, None
        self.health_sprite, self.health_label = None, None

        super().__init__(weapon, position, scale, **kwargs)

    def _build_components(self):
        image = try_load_image(self.entity.get_image_name(), image_part=self.ImagePart)
        if image is not None:
            self.main_sprite = Sprite(image, pos(0.0, 0.0, base=self.SizeBase), scale=self.ImageScale)
            self.add(self.main_sprite, z=0)
        self.border_sprite = Sprite('Weapon.png', pos(0.0, 0.0, base=self.SizeBase), scale=0.60)
        self.add(self.border_sprite, z=1)
        self.attack_sprite = Sprite('WeaponAtk.png', pos(-0.58, -0.49, base=self.SizeBase), scale=0.30)
        self.add(self.attack_sprite, z=2)
        self.attack_label = hs_style_label('0', pos(-0.58, -0.41, base=self.SizeBase), font_size=24, anchor_y='center')
        self.add(self.attack_label, z=3)
        self.health_sprite = Sprite('WeaponHealth.png', pos(0.60, -0.44, base=self.SizeBase), scale=0.32)
        self.add(self.health_sprite, z=2)
        self.health_label = hs_style_label('0', pos(0.59, -0.40, base=self.SizeBase), font_size=24, anchor_y='center')
        self.add(self.health_label, z=3)

        self.sheathed_image = Sprite('WeaponSheathed.png', pos(0.0, 0.0, base=self.SizeBase), scale=0.60)
        self.add(self.sheathed_image, z=1)

    def update_status_border(self):
        # Weapons does not have status border.
        pass

    def update_content(self, **kwargs):
        super().update_content(**kwargs)

        self.attack_label.element.text = str(self.entity.attack)
        self.attack_label.element.color = self._get_attack_color()
        self.health_label.element.text = str(self.entity.health)
        self.health_label.element.color = self._get_health_color()
        if self.entity.sheathed:
            if self.main_sprite is not None:
                self.main_sprite.visible = False
            self.border_sprite.visible = False
            self.sheathed_image.visible = True
        else:
            if self.main_sprite is not None:
                self.main_sprite.visible = True
            self.border_sprite.visible = True
            self.sheathed_image.visible = False


__all__ = [
    'EntitySprite',
    'HandSprite',
    'MinionSprite',
    'HeroSprite',
    'HeroPowerSprite',
    'HeroPowerFullArtSprite',
    'WeaponSprite',
]
