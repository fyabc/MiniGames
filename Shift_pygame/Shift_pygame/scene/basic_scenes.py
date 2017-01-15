#! /usr/bin/python
# -*- coding: utf-8 -*-

import pygame.locals

from .scene import Scene
from ..element.text import Text
from ..element.group import Group
from ..handler.active_text import ActiveText
from ..utils.keymap import get_keymap, get_unique_key_event

__author__ = 'fyabc'


class MenuScene(Scene):
    def __init__(self, game, scene_id, targets):
        """

        :param game:
        :param scene_id:
        :param targets: A dict.
            keys: target scenes name.
            values: target scenes id.
        """

        # [NOTE] This must before the _add_key() call.
        self.targets = targets

        super().__init__(game, scene_id)

        self.active_group = Group(self.game)
        self.groups.append(self.active_group)

        self.add_action((pygame.locals.MOUSEBUTTONUP, 1), self.on_mouse_up_1)

    def add_active_element(self, *elements):
        self.handlers.extend(elements)
        self.active_group.add(*elements)

    def on_mouse_up_1(self, game, event, pre_sid, *args):
        # Find clicked button.
        for handler in self.handlers:
            if getattr(handler, 'clicked', None) is True:
                return handler.on_mouse_up_1(game, event, pre_sid, *args)
        return None


class MainMenu(MenuScene):
    def __init__(self, game, scene_id, targets):
        super().__init__(game, scene_id, targets)

        self.add_background(
            Text(self.game, self, 'Sh', (0.449, 0.15), font_size=50),
            Text(self.game, self, 'ift', (0.561, 0.15), fg_bg=(True, False), font_size=50),
        )

        self.add_active_element(
            ActiveText(self.game, self, 'Help(H)', (0.25, 0.7),
                       mouse_up_call=(lambda *args: targets['HelpMenu'])),
            ActiveText(self.game, self, 'Quit(Q)', (0.75, 0.7),
                       mouse_up_call=(lambda *args: self.QuitID)),
        )

    def _add_keys(self):
        super()._add_keys()

        km = get_keymap()

        for key in km['quit']:
            self.add_jump_action(get_unique_key_event(key), self.QuitID)
        for key in km['help']:
            self.add_jump_action(get_unique_key_event(key), self.targets['HelpMenu'])


class HelpMenu(MenuScene):
    def __init__(self, game, scene_id):
        super().__init__(game, scene_id, None)

        self.add_background(
            Text(self.game, self, 'Help', (0.5, 0.15), font_size=44),
            Text(self.game, self, 'Left: Go left', (0.5, 0.29), font_size=27),
            Text(self.game, self, 'Right: Go right', (0.5, 0.37), font_size=27),
            Text(self.game, self, 'Up: To another level on the door', (0.5, 0.45), font_size=27),
            Text(self.game, self, 'Space: Jump', (0.5, 0.53), font_size=27),
            Text(self.game, self, 'Shift: Shift to another world', (0.5, 0.61), font_size=27),
        )

        self.add_active_element(
            ActiveText(
                self.game, self,
                'Return(Q)', (0.5, 0.8),
                mouse_up_call=(lambda t, g, e, pre_sid, *args: pre_sid)
            )
        )

    def _add_keys(self):
        super()._add_keys()

        km = get_keymap()

        for key in km['quit']:
            self.add_action(get_unique_key_event(key), lambda g, e, pre_sid, *args: pre_sid)
