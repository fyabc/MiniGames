#! /usr/bin/python
# -*- coding: utf-8 -*-

import bisect
from collections import Counter

from cocos import scene, layer, draw
from pyglet.window import mouse

from .card_item import CardItem
from .card_sprite import CardSprite
from ...utils.message import info
from ...utils.package_io import all_cards
from ...utils.draw.cocos_utils.basic import pos, pos_y, Colors
from ...utils.draw.cocos_utils.active import ActiveLayer, ActiveLabel
from ...utils.draw.cocos_utils.layers import BackgroundLayer, BasicButtonsLayer

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
    SwitchY = 0.15

    # todo: Click (or right click) card sprite to add card?

    def __init__(self, ctrl):
        super().__init__(ctrl)

        # Card pages (each page contains some card_ids) to show.
        self.card_id_pages = []
        self.page_id = 0
        self.page_card_sprites = []

        for is_right in (False, True):
            self.add(ActiveLabel.hs_style(
                '[ {} ]'.format('→' if is_right else '←'),
                pos((self.PageL + self.PageR) / 2 + 0.05 * (1 if is_right else -1), self.SwitchY),
                callback=lambda is_right_=is_right: self._switch_card_page(1 if is_right_ else -1),
                font_size=28, anchor_x='center', anchor_y='center', bold=True,
            ), name='button_page_{}'.format('right' if is_right else 'left'))

    def on_enter(self):
        super().on_enter()

        # if isinstance(director.director.scene, transitions.TransitionScene):
        #     return

        self.page_id = 0
        self._refresh_card_id_pages()
        
    def on_exit(self):
        self._remove_card_page()
        return super().on_exit()

    def _refresh_card_id_pages(self):
        """Recalculate card id pages and refresh related sprites."""

        # Add more filters here.
        card_ids = sorted(all_cards().keys())
        page_size = self.PageSize[0] * self.PageSize[1]
        self.card_id_pages = [
            card_ids[i * page_size: (i + 1) * page_size]
            for i in range((len(card_ids) + page_size - 1) // page_size)
        ]
        self._switch_card_page()

    def _switch_card_page(self, delta_id=0):
        """Called when switch the card page.
        Remove old cards, add new cards.
        """
        self.page_id = min(max(0, self.page_id + delta_id), len(self.card_id_pages) - 1)
        current_page = self.card_id_pages[self.page_id]

        self._remove_card_page()

        for i, card_id in enumerate(current_page):
            x, y = i % self.PageSize[0], i // self.PageSize[0]
            # todo: Change these static card sprites into original card paintings?
            card_sprite = CardSprite(
                card_id, pos(self.PageL + (self.PageR - self.PageL) * (2 * x + 1) / (2 * self.PageSize[0]),
                             self.PageT + (self.PageB - self.PageT) * (2 * y + 1) / (2 * self.PageSize[1]))
                , is_front=True, scale=0.5, callback=self._get_card_callbacks(card_id),
                # selected_effect=None, unselected_effect=None,
            )
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
    CardListT = 0.88
    CardListB = 0.25
    CardShowS = 15

    def __init__(self, ctrl):
        super().__init__(ctrl)
        self.deck_id = None
        self.deck = None    # Local copy of edit deck.
        self.delete_deck = False

        # Sorted card items.
        # (cost, card_id, card_item)
        self.card_items = []
        self.card_show_start = None

        self.label_deck_name = ActiveLabel.hs_style(
            '', pos(self.DeckC, self.DeckTitleY), anchor_x='center', anchor_y='center',
            bold=True,
        )
        self.add(self.label_deck_name, name='label_deck_name')

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
            # todo: Add new deck
            self.deck_id = 0

        self.deck = self.ctrl.user.decks[self.deck_id].copy()
        self.card_show_start = 0

        self.label_deck_name.element.text = self.deck.name
        self._build_card_items()
        self._refresh_card_items()

    def on_exit(self):
        # Store card items into deck
        decks = self.ctrl.user.decks
        if self.delete_deck:
            if self.deck_id == 'new':
                info('New deck {} not saved.'.format(self.deck))
            else:
                del self.ctrl.user.decks[self.deck_id]
                info('Deck {} {} deleted.'.format(self.deck_id, decks[self.deck_id]))
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

        self.label_deck_name.element.text = ''
        self._remove_card_items()
        self.card_items.clear()

        return super().on_exit()

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
