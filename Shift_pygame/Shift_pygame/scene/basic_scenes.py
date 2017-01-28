#! /usr/bin/python
# -*- coding: utf-8 -*-

import pygame.locals

from ..config import GameGroups, SceneTitleLocation, DefaultGroup, FontMedium
from .scene import Scene
from ..element.text import Text
from ..element.group import Group
from ..handler.active_text import ActiveText
from ..utils.keymap import get_keymap, get_unique_key_event

__author__ = 'fyabc'


class MenuScene(Scene):
    """The base class of menu scenes.

    Menu scene contains some background text, some active text (button), etc.
    Menu scene is a handler for mouse button 1 (left) click events and key events in keymap.
    """

    def __init__(self, game, scene_id, targets):
        """

        :param game:
        :param scene_id:
        :param targets: A dict.
            keys: target scenes name.
            values: target scenes id.
        """

        super().__init__(game, scene_id, targets)

        self.active_group = Group(self.game)
        self.groups.append(self.active_group)

        self.add_action((pygame.locals.MOUSEBUTTONUP, 1), self.on_mouse_up_1)

        self._add_elements()

    def _add_elements(self):
        """Subclasses override this method to add elements."""
        pass

    def add_active_element(self, *elements):
        self.handlers.extend(elements)
        self.active_group.add(*elements)

    def on_mouse_up_1(self, scene, event, pre_sid, *args):
        # Find clicked button.
        for handler in self.handlers:
            if getattr(handler, 'clicked', None) is True:
                return handler.on_mouse_up_1(scene, event, pre_sid, *args)
        return None


class MainMenu(MenuScene):
    """The main menu after start the game."""

    def _add_elements(self):
        self.add_background(
            Text(self.game, self, 'Sh', (0.449, 0.15)),
            Text(self.game, self, 'ift', (0.561, 0.15), fg_bg=(True, False), font_size=50),
        )

        def _open_github(*args):
            import webbrowser
            webbrowser.open('http://github.com/fyabc/MiniGames/tree/master/Shift_pygame')
            return self.targets['MainMenu']

        self.add_active_element(
            ActiveText(self.game, self, 'Select Game', (0.25, 0.4),
                       on_mouse_up=(lambda *args: self.targets['GameSelectMenu'])),
            ActiveText(self.game, self, 'Help(H)', (0.25, 0.7),
                       on_mouse_up=(lambda *args: self.targets['HelpMenu'])),
            ActiveText(self.game, self, 'Quit(Q)', (0.75, 0.7),
                       on_mouse_up=(lambda *args: self.QuitID)),
            ActiveText(self.game, self, 'Author: fyabc<www.github.com/fyabc>', (0.5, 0.9), font_size=20,
                       on_mouse_up=_open_github),
        )

    def _add_keys(self):
        super()._add_keys()

        km = get_keymap()

        for key in km['quit']:
            self.add_jump_action(get_unique_key_event(key), self.QuitID)
        for key in km['help']:
            self.add_jump_action(get_unique_key_event(key), self.targets['HelpMenu'])


class HelpMenu(MenuScene):
    """The help menu. This menu may also be used as pause menu."""

    def _add_elements(self):
        self.add_background(
            Text(self.game, self, 'Help', SceneTitleLocation),
            Text(self.game, self, 'Left: Go left', (0.5, 0.29), font_size=FontMedium),
            Text(self.game, self, 'Right: Go right', (0.5, 0.37), font_size=FontMedium),
            Text(self.game, self, 'Up: To another level on the door', (0.5, 0.45), font_size=FontMedium),
            Text(self.game, self, 'Space: Jump', (0.5, 0.53), font_size=FontMedium),
            Text(self.game, self, 'Shift: Shift to another world', (0.5, 0.61), font_size=FontMedium),
        )

        self.add_active_element(
            ActiveText(self.game, self, 'Return(Q)', (0.5, 0.8),
                       on_mouse_up=(lambda t, s, e, pre_sid, *args: pre_sid))
        )

    def _add_keys(self):
        super()._add_keys()

        km = get_keymap()

        for key in km['quit']:
            self.add_action(get_unique_key_event(key), lambda s, e, pre_sid, *args: pre_sid)


class GameSelectMenu(MenuScene):
    """The game group select scene. Open from 'Select Game' in main menu."""

    def _add_elements(self):
        self.add_background(
            Text(self.game, self, 'Select Game', SceneTitleLocation),
        )

        game_group_number = len(GameGroups)

        for i, game_group_name in enumerate(GameGroups):
            def _on_mouse_up(*args, game_group_name_=game_group_name):
                return self.targets['GameMainMenu'], game_group_name_

            self.add_active_element(
                ActiveText(self.game, self, game_group_name, (0.2, 0.3 + 0.07 * i), font_size=FontMedium,
                           on_mouse_up=_on_mouse_up)
            )

    def _add_keys(self):
        super()._add_keys()

        km = get_keymap()

        for key in km['quit']:
            self.add_jump_action(get_unique_key_event(key), self.targets['MainMenu'])


class GameMainMenu(MenuScene):
    """The main menu of the game. After the game select menu."""

    def __init__(self, game, scene_id, targets):
        super().__init__(game, scene_id, targets)

        self.game_group_name = DefaultGroup

    def _add_elements(self):
        self.title = Text(self.game, self, 'Game Options', SceneTitleLocation)

        self.add_background(
            self.title,
        )

        self.add_active_element(
            ActiveText(self.game, self, 'New Game', (0.5, 0.3), font_size=FontMedium,
                       on_mouse_up=lambda *args: (self.targets['LevelSelectMenu'], self.game_group_name)),
            ActiveText(self.game, self, 'Continue', (0.5, 0.5), font_size=FontMedium,
                       on_mouse_up=lambda *args: (self.targets['LevelSelectMenu'], self.game_group_name)),
            ActiveText(self.game, self, 'Return(Q)', (0.5, 0.7), font_size=FontMedium,
                       on_mouse_up=lambda *args: self.targets['GameSelectMenu']),
        )

    def _add_keys(self):
        super()._add_keys()

        km = get_keymap()

        for key in km['quit']:
            self.add_jump_action(get_unique_key_event(key), self.targets['GameSelectMenu'])

    def run(self, previous_scene_id, *args):
        """

        :param previous_scene_id: as default
        :param args:
            args[0] = game_group_name
        :return:
        """

        # Load game group name, do some works.
        self.game_group_name = args[0]
        self.title.set_text('Game Options: {}'.format(self.game_group_name))

        return super().run(previous_scene_id, *args)

    def draw_background(self):
        super().draw_background()

        # todo: Add level buttons (even link graph) into the scene


class LevelSelectMenu(MenuScene):
    """The menu for level selection.

    It contains level numbers (maybe also contains their connections).

    Click the levels will go to level scene (game scene).
    """

    def __init__(self, game, scene_id, targets):
        super().__init__(game, scene_id, targets)

        self.game_group_name = DefaultGroup

    def _add_keys(self):
        super()._add_keys()

        km = get_keymap()

        for key in km['quit']:
            self.add_action(get_unique_key_event(key),
                            lambda s, *args: (self.targets['GameSelectMenu'], s.game_group_name))

    def _add_level_buttons(self):
        game_group_data = self.game.game_groups_data[self.game_group_name]
        for i, level_data in game_group_data.levels.items():
            y, x = divmod(i - 1, 5)

            def _on_mouse_up(*args, i_=i):
                return self.targets['LevelScene'], self.game_group_name, i_

            text = str(i)
            loc = (0.1 + 0.2 * x, 0.2 + 0.1 * y)

            if level_data.reached:
                self.add_active_element(
                    ActiveText(self.game, self, text, loc, font_size=FontMedium,
                               on_mouse_up=_on_mouse_up)
                )
            else:
                self.add_background(
                    Text(self.game, self, text, loc, fg_bg=(True, False), font_size=FontMedium)
                )

    def run(self, previous_scene_id, *args):
        """

        :param previous_scene_id: as default
        :param args:
            args[0] = game_group_name
        :return:
        """

        self.game_group_name = args[0]

        self._add_level_buttons()

        return super().run(previous_scene_id, *args)
