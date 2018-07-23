#! /usr/bin/python
# -*- coding: utf-8 -*-

import bisect
from collections import Counter

from cocos import scene, layer, draw, rect
from pyglet.window import mouse

from .card_sprite import HandSprite
from .collection_sprites import StaticCardSprite, CardItem
from .utils.active import ActiveLayer, ActiveLabel, ActiveSprite, set_color_action
from .utils.basic import pos, pos_x, pos_y, Colors, hs_style_label, try_load_image
from .utils.layers import BackgroundLayer, BasicButtonsLayer, DialogLayer
from .utils.primitives import Rect
from ...game.deck import Deck
from ...utils.game import Klass
from ...utils.message import info
from ...utils.package_io import all_cards

__author__ = 'fyabc'

DeckSelectID, DeckEditID = 0, 1


class CollectionsBBLayer(BasicButtonsLayer):
    """Wrap the basic buttons layer, modify actions when return in deck edit mode.
    Current solution: switch to deck selection mode to ensure save.
    """

    def go_back(self):
        self.parent.get('deck').switch_to(DeckSelectID)
        return super().go_back()

    def goto_options(self):
        self.parent.get('deck').switch_to(DeckSelectID)
        return super().goto_options()


class CollectionsLayer(ActiveLayer):
    CollectionsR = 0.8
    PageSize = (4, 2)
    PageT = 0.9
    PageB = 0.25
    PageL = 0.05
    PageR = CollectionsR - 0.05
    KlassIconY = 0.94
    KlassIconDeltaX = 0.05
    KlassIconL, KlassIconR = PageL, PageL + (Klass.NumEnums - 1) * KlassIconDeltaX
    KlassIconScale = 1.0
    KlassIconSize = 48 * KlassIconScale
    SwitchY = 0.15

    # Use ``StaticCardSprite`` or ``HandSprite``.
    UseStaticSprite = False

    KlassOrder = {
        k: v for v, k in enumerate([
            Klass.Druid, Klass.Hunter, Klass.Mage,
            Klass.Paladin, Klass.Priest, Klass.Rogue,
            Klass.Shaman, Klass.Warlock, Klass.Warrior,
            Klass.Monk, Klass.DeathKnight, Klass.Neutral,
        ])
    }
    KlassOrderR = {v: k for k, v in KlassOrder.items()}

    def __init__(self, ctrl):
        super().__init__(ctrl)

        # Card pages (each page contains some card_ids) to show.
        self.card_id_pages = []

        # Page list groups: Klass ID -> page list
        self.page_list_groups = {
            k: [] for k in self.KlassOrder
        }
        # Current klass id. By default klass of group 0.
        self.klass_id = self.KlassOrderR[0]
        # Current page id.
        self.page_id = 0

        # Sprites of current page, and cache of all card sprites.
        self.page_card_sprites = []
        self.card_cache = {}

        # Class icons and activated marker.
        _rect = rect.Rect(0, 0, self.KlassIconSize, self.KlassIconSize)
        _rect.center = pos(self.KlassIconL, self.KlassIconY)
        self.klass_icon_activated = Rect(_rect, color=Colors['orange'], width=2)
        self.add(self.klass_icon_activated)

        self.klass_icons = {}
        for klass_name, klass in Klass.Str2Idx.items():
            # [NOTE]: These icons may be hidden if not any cards.
            i = self.KlassOrder[klass]
            icon = ActiveSprite(
                try_load_image('ClassIcon-{}.png'.format(klass_name), default='ClassIcon-Neutral.png'),
                pos(self.KlassIconL + i * self.KlassIconDeltaX, self.KlassIconY),
                callback=lambda klass_=klass: self.set_klass_id(klass_, refresh_page=True, silent_same=True),
                scale=1.0
            )
            self.klass_icons[klass] = icon
            self.add(icon)

        for is_right in (False, True):
            self.add(ActiveLabel.hs_style(
                '[ {} ]'.format('→' if is_right else '←'),
                pos((self.PageL + self.PageR) / 2 + 0.05 * (1 if is_right else -1), self.SwitchY),
                callback=self._next_card_page if is_right else self._previous_card_page,
                font_size=28, anchor_x='center', anchor_y='center', bold=True,
            ), name='button_page_{}'.format('right' if is_right else 'left'))

    def on_enter(self):
        super().on_enter()

        # if isinstance(director.director.scene, transitions.TransitionScene):
        #     return

        self._refresh_card_id_pages()
        
    def on_exit(self):
        # [NOTE]: Not clear cache when exit the collections layer.
        self._remove_card_page()
        return super().on_exit()

    def _create_card_sprite(self, card_id, x, y):
        """Create a card sprite from card image, or create a "blank" sprite if image not exists."""
        from pyglet.resource import ResourceNotFoundException
        position = pos(self.PageL + (self.PageR - self.PageL) * (2 * x + 1) / (2 * self.PageSize[0]),
                       self.PageT + (self.PageB - self.PageT) * (2 * y + 1) / (2 * self.PageSize[1]))
        callback = self._get_card_callbacks(card_id)
        sel_mgr_kwargs = {'move_to_top': True}

        result = self.card_cache.get(card_id, None)
        if result is not None:
            # Only need to modify position.
            result.position = position
            return result

        def _mk_hand_sprite():
            sprite = HandSprite(
                card_id, position,
                is_front=True, scale=0.5, callback=callback,
                sel_mgr_kwargs=sel_mgr_kwargs,
            )
            self.card_cache[card_id] = sprite
            return sprite

        if not self.UseStaticSprite:
            return _mk_hand_sprite()

        try:
            card_sprite = StaticCardSprite(
                card_id, position,
                scale=0.61, callback=callback,
                sel_mgr_kwargs=sel_mgr_kwargs,
            )
            self.card_cache[card_id] = card_sprite
        except ResourceNotFoundException:
            card_sprite = _mk_hand_sprite()
        return card_sprite

    @classmethod
    def _card_order(cls, e):
        data = e[1].data
        return data['cost'], data['type'], data.get('attack', 0), data.get('health', 0), data['id']

    def _refresh_card_id_pages(self):
        """Recalculate card id pages and refresh related sprites."""

        id_card_groups = {klass: [] for klass in self.KlassOrder}
        for k, v in all_cards().items():
            if v.data['derivative']:
                continue
            id_card_groups[v.data['klass']].append((k, v))
        # Add more filters here.

        card_id_groups = {
            klass: [k for k, v in sorted(id_card_group, key=self._card_order)]
            for klass, id_card_group in id_card_groups.items()
        }

        page_size = self.PageSize[0] * self.PageSize[1]
        self.page_list_groups = {
            klass: [
                card_id_group[i * page_size: (i + 1) * page_size]
                for i in range((len(card_id_group) + page_size - 1) // page_size)
            ]
            for klass, card_id_group in card_id_groups.items() if card_id_group
        }

        # Get the first available klass.
        klass_order = self.KlassOrder[self.klass_id]
        while self.KlassOrderR[klass_order] not in self.page_list_groups:
            klass_order += 1
        self.set_klass_id(self.KlassOrderR[klass_order], refresh_page=True)

        self._refresh_klass_icons()

    def _refresh_klass_icons(self):
        i = 0
        for order in range(len(self.KlassOrderR)):
            klass = self.KlassOrderR[order]
            icon = self.klass_icons[klass]
            if klass in self.page_list_groups:
                icon.visible = True
                icon.x = pos_x(self.KlassIconL + i * self.KlassIconDeltaX)
                i += 1
            else:
                icon.visible = False

    def set_klass_id(self, klass, refresh_page=False, silent_same=False):
        if silent_same and self.klass_id == klass:
            return
        self.klass_id = klass
        self.klass_icon_activated.set_rect_attr('center', self.klass_icons[klass].position)

        if refresh_page:
            self._switch_card_page2(0)

    def _switch_card_page2(self, page_id):
        self.page_id = page_id
        current_page = self.page_list_groups[self.klass_id][self.page_id]

        self._remove_card_page()

        for i, card_id in enumerate(current_page):
            x, y = i % self.PageSize[0], i // self.PageSize[0]
            card_sprite = self._create_card_sprite(card_id, x, y)
            self.page_card_sprites.append(card_sprite)
            self.add(card_sprite)

    def _next_card_page(self):
        page_id = self.page_id + 1
        if page_id == len(self.page_list_groups[self.klass_id]):
            klass_order = self.KlassOrder[self.klass_id] + 1
            # Skip empty klasses.
            while self.KlassOrderR[klass_order] not in self.page_list_groups:
                klass_order += 1
            if klass_order == len(self.KlassOrder):
                # Hit the end
                return
            self.set_klass_id(self.KlassOrderR[klass_order], refresh_page=False)
            self._switch_card_page2(0)
        else:
            self._switch_card_page2(page_id)

    def _previous_card_page(self):
        page_id = self.page_id - 1
        if page_id == -1:
            klass_order = self.KlassOrder[self.klass_id] - 1
            while self.KlassOrderR[klass_order] not in self.page_list_groups:
                klass_order -= 1
            if klass_order == -1:
                # Hit the start
                return
            new_klass_id = self.KlassOrderR[klass_order]
            self.set_klass_id(new_klass_id, refresh_page=False)
            self._switch_card_page2(len(self.page_list_groups[new_klass_id]) - 1)
        else:
            self._switch_card_page2(page_id)

    def _switch_card_page(self, delta_id=0):
        """Called when switch the card page.
        Remove old cards, add new cards.
        """
        self.page_id = min(max(0, self.page_id + delta_id), len(self.card_id_pages) - 1)
        current_page = self.card_id_pages[self.page_id]

        self._remove_card_page()

        for i, card_id in enumerate(current_page):
            x, y = i % self.PageSize[0], i // self.PageSize[0]
            card_sprite = self._create_card_sprite(card_id, x, y)
            self.page_card_sprites.append(card_sprite)
            self.add(card_sprite)

    def _remove_card_page(self, clear=True):
        for card_sprite in self.page_card_sprites:
            if card_sprite in self:
                self.remove(card_sprite)
        if clear:
            self.page_card_sprites.clear()

    def _get_card_callbacks(self, card_id):
        def _left():
            multiplex_layer = self.ctrl.get_node('collection/deck')
            if multiplex_layer.enabled_layer == DeckSelectID:
                return
            else:
                multiplex_layer.layers[multiplex_layer.enabled_layer].on_card_clicked(card_id)
                return True

        def _right():
            print('right')
        return {
            mouse.LEFT: _left,
            mouse.RIGHT: _right,
        }


class DeckSelectLayer(ActiveLayer):
    DeckL = CollectionsLayer.CollectionsR
    DeckC = (1 + DeckL) / 2
    DeckListT = 0.9
    DeckListB = 0.25
    DeckShowS = 10
    UpDownY = 0.11

    def __init__(self, ctrl):
        super().__init__(ctrl)

        self.deck_show_start = 0
        self.deck_button_list = []

        for is_down in (False, True):
            self.add(ActiveLabel.hs_style(
                '[ {} ]'.format('↓' if is_down else '↑'),
                pos(self.DeckC + 0.05 * (1 if is_down else -1), self.UpDownY),
                callback=lambda is_down_=is_down: self.scroll_deck(is_down_),
                font_size=28, anchor_x='center', anchor_y='center', bold=True,
            ), name='button_decks_{}'.format('down' if is_down else 'up'))

    def on_enter(self):
        super().on_enter()

        self.deck_show_start = 0
        self.deck_button_list = [
            ActiveLabel.hs_style(
                deck.name, pos(self.DeckC, 1.0),
                callback=lambda deck_id_=i: self.on_select_deck(deck_id_),
                anchor_x='center', anchor_y='center')
            for i, deck in enumerate(self.ctrl.user.decks)
        ]
        self.deck_button_list.append(ActiveLabel.hs_style(
            '[新套牌]', pos(self.DeckC, 1.0),
            callback=lambda: self.on_select_deck('new'), anchor_x='center', anchor_y='center',
            bold=True,
        ))
        self._refresh_deck_buttons()

    def on_exit(self):
        self._remove_deck_buttons()
        self.deck_button_list.clear()
        self.deck_show_start = 0

        return super().on_exit()

    def _refresh_deck_buttons(self):
        for i, deck_button in enumerate(self.deck_button_list):
            deck_button.y = pos_y(self.DeckListT - (self.DeckListT - self.DeckListB) *
                                  (i - self.deck_show_start) / (self.DeckShowS - 1))
            if self.deck_show_start <= i < self.deck_show_start + self.DeckShowS:
                if deck_button not in self:
                    self.add(deck_button)
            else:
                if deck_button in self:
                    self.remove(deck_button)

    def _remove_deck_buttons(self):
        for deck_button in self.deck_button_list:
            if deck_button in self:
                self.remove(deck_button)

    def on_select_deck(self, deck_id):
        self.parent.layers[DeckEditID].deck_id = deck_id
        self.parent.switch_to(DeckEditID)

    def scroll_deck(self, is_down):
        if is_down:
            if self.deck_show_start + self.DeckShowS >= len(self.deck_button_list):
                return
        else:
            if self.deck_show_start == 0:
                return
        self.deck_show_start += int(is_down) * 2 - 1
        self._refresh_deck_buttons()


class DeckEditLayer(ActiveLayer):
    DeckL, DeckC = DeckSelectLayer.DeckL, DeckSelectLayer.DeckC
    DeckTitleY = 0.94
    UpDownY = 0.19
    EditDoneY = 0.11
    CardListT = 0.86
    CardListB = 0.25
    CardShowS = 15
    TitleImagePart = (0.20, 0.72, 0.63, 0.135)

    def __init__(self, ctrl):
        super().__init__(ctrl)
        self.deck_id = None
        self.deck = None    # Local copy of edit deck.
        self.delete_deck = False

        # Sorted card items.
        # (cost, card_id, card_item)
        self.card_items = []
        self.card_show_start = None

        # [NOTE]: If you want to change the image, must ensure that the image size is same,
        # or the position will be incorrect.
        self.sprite_deck_name = ActiveSprite(
            try_load_image('1000000.png', image_part=self.TitleImagePart), callback=self.on_title_clicked, scale=1.5)
        self.sprite_deck_name.visible = False
        self.add(self.sprite_deck_name, name='sprite_deck_name')
        self.label_deck_name = ActiveLabel.hs_style(
            '', pos(self.DeckL, self.DeckTitleY), anchor_x='left', anchor_y='top',
            bold=True, font_size=22,
        )
        self.label_deck_name.visible = False
        self.add(self.label_deck_name, name='label_deck_name', z=1)

        for is_down in (False, True):
            self.add(ActiveLabel.hs_style(
                '[ {} ]'.format('↓' if is_down else '↑'),
                pos(self.DeckC + 0.05 * (1 if is_down else -1), self.UpDownY),
                callback=lambda is_down_=is_down: self.scroll_card_list(is_down_),
                font_size=28, anchor_x='center', anchor_y='center', bold=True,
            ), name='button_card_{}'.format('down' if is_down else 'up'))
        self.add(ActiveLabel.hs_style(
            '[完成]', pos(self.DeckC, self.EditDoneY),
            callback=self.on_edit_done, anchor_x='center', anchor_y='center',
            bold=True,
        ), name='edit_done')

    def on_enter(self):
        super().on_enter()

        assert self.deck_id is not None, 'Deck not selected correctly'

        if self.deck_id == 'new':
            # New deck dialog.
            DW, DH = 0.7, 0.7
            layer_ = DialogLayer(Colors['black'], *map(int, pos(DW, DH)),
                                 position=pos((1 - DW) / 2, (1 - DH) / 2), stop_event=True, border=True)
            layer_.add(hs_style_label('选择职业', pos(DW * 0.5, DH * 0.98), anchor_y='top'))

            def _on_done(klass):
                layer_.remove_from_scene()
                self.deck = Deck(klass=klass, card_id_list=[], mode='standard')
                self._on_deck_opened()

            def _on_canceled():
                layer_.remove_from_scene()
                self.on_edit_done()

            NColumns = 3
            NRows = (len(Klass.Idx2Str) - 1) // NColumns + 1
            i = 0
            for (kls, name) in Klass.Idx2Str.items():
                if kls == Klass.Neutral:
                    continue
                y, x = divmod(i, NColumns)
                layer_.add(ActiveLabel.hs_style(
                    name, pos((2 * x + 1) / (2 * NColumns) * DW,
                              (0.04 + 0.92 * (2 * (NRows - y - 1) + 1) / (2 * NRows)) * DH),
                    anchor_x='center', anchor_y='center', callback=lambda kls_=kls: _on_done(kls_),
                ))
                i += 1

            layer_.add(ActiveLabel.hs_style(
                '取消', pos(0.5 * DW, 0.02 * DH), anchor_x='center', anchor_y='bottom',
                callback=_on_canceled,
            ))
            layer_.add_to_scene(self.parent)
        else:
            # Open an exist deck.
            self.deck = self.ctrl.user.decks[self.deck_id].copy()
            self._on_deck_opened()

    def on_exit(self):
        # Store card items into deck
        decks = self.ctrl.user.decks

        # If new deck operation is canceled, ``self.deck`` will be ``None``.
        if self.deck is None:
            self.deck_id = None
            return super().on_exit()

        if self.delete_deck:
            if self.deck_id == 'new':
                info('New deck {} not saved.'.format(self.deck))
            else:
                info('Deck {} {} deleted.'.format(self.deck_id, decks[self.deck_id]))
                del self.ctrl.user.decks[self.deck_id]
        else:
            if self.deck_id == 'new':
                decks.append(self.deck)
                info('New deck {} saved.'.format(self.deck))
            else:
                decks[self.deck_id] = self.deck
                info('Deck {} {} saved.'.format(self.deck_id, decks[self.deck_id]))

        self.deck_id = None
        self.deck = None
        self.card_show_start = None

        self.sprite_deck_name.visible = False
        self.label_deck_name.visible = False
        self._remove_card_items()
        self.card_items.clear()

        return super().on_exit()

    def _on_deck_opened(self):
        """Callback called when deck completely opened or created."""

        self.card_show_start = 0

        self.label_deck_name.element.text = self.deck.name
        self.label_deck_name.visible = True

        image = try_load_image(
            'Hero-{}.png'.format(self.ctrl.user.class_hero_map[self.deck.klass]), image_part=self.TitleImagePart)
        if image is not None:
            self.sprite_deck_name.image = image
        self.sprite_deck_name.position = pos(self.DeckC, self.DeckTitleY)
        self.sprite_deck_name.visible = True

        self._build_card_items()
        self._refresh_card_items()

    def _build_card_items(self):
        card_cnt = Counter(self.deck.card_id_list)
        self.card_items = sorted(
            [all_cards()[card_id].data['cost'], card_id,
             CardItem(card_id, n, pos(self.DeckC, 0), scale=1.0,
                      callback=self.on_card_item_clicked, self_in_callback=True)]
            for card_id, n in card_cnt.items())

    def _refresh_card_items(self):
        for i, (_, _, card_item) in enumerate(self.card_items):
            card_item.y = pos_y(self.CardListT - (self.CardListT - self.CardListB) *
                                (i - self.card_show_start) / (self.CardShowS - 1))
            if self.card_show_start <= i < self.card_show_start + self.CardShowS:
                if card_item not in self:
                    self.add(card_item)
            else:
                if card_item in self:
                    self.remove(card_item)

    def _remove_card_item(self, card_item: CardItem):
        self.card_items.remove([card_item.get_card().data['cost'], card_item.card_id, card_item])
        if card_item in self:
            self.remove(card_item)

    def _remove_card_items(self):
        for _, _, card_item in self.card_items:
            if card_item in self:
                self.remove(card_item)

    def scroll_card_list(self, is_down):
        if is_down:
            if self.card_show_start + self.CardShowS >= len(self.card_items):
                return
        else:
            if self.card_show_start == 0:
                return
        self.card_show_start += int(is_down) * 2 - 1
        self._refresh_card_items()

    def on_edit_done(self):
        self.parent.switch_to(DeckSelectID)

    def on_title_clicked(self):
        from .utils.layers import LineEditLayer
        DW, DH = 0.5, 0.2

        def _ok():
            self.label_deck_name.element.text = self.deck.name = layer_.deck_name
            layer_.remove_from_scene()

        def _delete():
            # TODO: Add confirm
            self.delete_deck = True
            layer_.remove_from_scene()
            self.on_edit_done()

        layer_ = LineEditLayer(Colors['black'], *map(int, pos(DW, DH)),
                               position=pos((1 - DW) / 2, (1 - DH) / 2), stop_event=True, border=True)
        layer_.deck_name = self.deck.name
        layer_.add(ActiveLabel.hs_style(
            '删除卡组', pos(0.3 * DW, 0.05 * DH), anchor_x='center',
            callback=_delete,
            color=Colors['red'],
            unselected_effect=set_color_action(Colors['red']),
        ))
        layer_.add_ok(_ok, position=(0.7, 0.05))
        layer_.add_to_scene(self.parent)

    def on_card_item_clicked(self, card_item: CardItem):
        """Click an card item, will remove one card."""

        n = card_item.n
        if n > 1:
            card_item.n = n - 1
        else:
            self._remove_card_item(card_item)
        self._refresh_card_items()
        self.deck.card_id_list.remove(card_item.card_id)
        return True

    def on_card_clicked(self, card_id):
        if card_id in self.deck.card_id_list:
            for _, c_id, item in self.card_items:
                if c_id == card_id:
                    item.n += 1
                    break
        else:
            new_entry = [
                all_cards()[card_id].data['cost'], card_id,
                CardItem(card_id, 1, pos(self.DeckC, 0), scale=1.0,
                         callback=self.on_card_item_clicked, self_in_callback=True)]
            bisect.insort(self.card_items, new_entry)
            self.add(new_entry[2])
        self._refresh_card_items()
        self.deck.card_id_list.append(card_id)


def get_collection_bg():
    deck_l = DeckSelectLayer.DeckL

    bg = BackgroundLayer()
    bg.add(draw.Line(pos(deck_l, 0.0), pos(deck_l, 1.0), Colors['white'], 2))

    return bg


def get_collection_scene(controller):
    collection_scene = scene.Scene()
    collection_scene.add(get_collection_bg(), z=0, name='background')
    collection_scene.add(CollectionsBBLayer(controller), z=1, name='basic_buttons')
    collection_scene.add(CollectionsLayer(controller), z=2, name='collections')
    collection_scene.add(layer.MultiplexLayer(
        DeckSelectLayer(controller),
        DeckEditLayer(controller),
    ), z=3, name='deck')

    return collection_scene


__all__ = [
    'get_collection_scene',
]
