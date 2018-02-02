#! /usr/bin/python
# -*- coding: utf-8 -*-

from cocos import scene, layer

from .card_item import CardItem
from ...utils.message import info
from ...utils.draw.cocos_utils.basic import pos, pos_y
from ...utils.draw.cocos_utils.active import ActiveLayer, ActiveLabel
from ...utils.draw.cocos_utils.layers import BackgroundLayer, BasicButtonsLayer

__author__ = 'fyabc'


class CollectionsBBLayer(BasicButtonsLayer):
    """Wrap the basic buttons layer, modify actions when return in deck edit mode.
    Current solution: switch to deck selection mode to ensure save.
    """

    def go_back(self):
        self.parent.get('deck').switch_to(0)
        return super().go_back()

    def goto_options(self):
        self.parent.get('deck').switch_to(0)
        return super().goto_options()


class CollectionsLayer(ActiveLayer):
    CollectionsR = 0.8

    def __init__(self, ctrl):
        super().__init__(ctrl)


class DeckSelectLayer(ActiveLayer):
    DeckL = CollectionsLayer.CollectionsR
    DeckC = (1 + DeckL) / 2
    DeckListTop = 0.9
    DeckListBottom = 0.25
    DeckShowSize = 10

    def __init__(self, ctrl):
        super().__init__(ctrl)

        self.deck_show_start = 0
        self.deck_button_list = []

        for is_down in (False, True):
            self.add(ActiveLabel.hs_style(
                '[ {} ]'.format('↓' if is_down else '↑'),
                pos(self.DeckC + 0.05 * (1 if is_down else -1), 0.15),
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
            callback=self.on_new_deck, anchor_x='center', anchor_y='center',
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
            deck_button.y = pos_y(self.DeckListTop - (self.DeckListTop - self.DeckListBottom) *
                                  (i - self.deck_show_start) / (self.DeckShowSize - 1))
            if self.deck_show_start <= i < self.deck_show_start + self.DeckShowSize:
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
        self.parent.layers[1].deck_id = deck_id
        self.parent.switch_to(1)

    def on_new_deck(self):
        info('Creating new deck')
        pass

    def scroll_deck(self, is_down):
        if is_down:
            if self.deck_show_start + self.DeckShowSize >= len(self.deck_button_list):
                return
        else:
            if self.deck_show_start == 0:
                return
        self.deck_show_start += int(is_down) * 2 - 1
        self._refresh_deck_buttons()


class DeckEditLayer(ActiveLayer):
    DeckL, DeckC = DeckSelectLayer.DeckL, DeckSelectLayer.DeckC

    def __init__(self, ctrl):
        super().__init__(ctrl)
        self.deck_id = None
        self.delete_deck = False

        self.card_items = []

        self.add(ActiveLabel.hs_style(
            '[完成]', pos(self.DeckC, 0.15),
            callback=self.on_edit_done, anchor_x='center', anchor_y='center',
            bold=True,
        ), name='edit_done')

    def on_enter(self):
        super().on_enter()

        assert self.deck_id is not None, 'Deck not selected correctly'

        deck = self.ctrl.user.decks[self.deck_id]

    def on_exit(self):
        # Store card items into deck
        decks = self.ctrl.user.decks
        if self.delete_deck:
            info('Deck {} {} deleted.'.format(self.deck_id, decks[self.deck_id]))
            del self.ctrl.user.decks[self.deck_id]
        else:
            info('Deck {} {} saved.'.format(self.deck_id, decks[self.deck_id]))
            # todo

        self.deck_id = None
        self._remove_card_items()
        self.card_items.clear()

        return super().on_exit()

    def _refresh_card_items(self):
        pass

    def _remove_card_items(self):
        pass

    def on_edit_done(self):
        self.parent.switch_to(0)


def get_collection_scene(controller):
    collection_scene = scene.Scene()
    collection_scene.add(BackgroundLayer(), z=0, name='background')
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
