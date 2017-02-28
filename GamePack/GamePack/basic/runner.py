#! /usr/bin/python
# -*- encoding: utf-8 -*-

from contextlib import contextmanager

import pygame

from ..utils.constant import ScreenSize, FontName
from ..utils.basic import load_image
from ..utils.path import get_data_path

__author__ = 'fyabc'


class PygameRunner:
    """A simple class of pygame runner.

    It wrap some necessary works and simplify the code.
    This class should be inherited and be used as a singleton.
    """

    def __init__(self, **kwargs):
        self.screen_size = kwargs.pop('screen_size', ScreenSize)
        self.allow_events = kwargs.pop('allow_events', ())
        self.name = kwargs.pop('name', 'Game')

        self.main_window = None
        self.timer = None

        # The dict of all used images, keys are image name and size.
        self.images = {}
        # The dict of all used fonts, keys are font size and image.
        self.fonts = {}

    def init(self):
        if self.main_window is not None:
            return

        pygame.init()

        self.main_window = pygame.display.set_mode(self.screen_size)
        self.timer = pygame.time.Clock()

        pygame.display.set_caption(self.name)

        pygame.event.set_allowed(self.allow_events)

        self.images.clear()
        self.fonts.clear()

    @contextmanager
    def _game_manager(self):
        self.init()

        yield

        pygame.quit()

        print('The game is quited!')

        exit(0)

    def run(self):
        with self._game_manager():
            self.main_loop()

    def main_loop(self):
        """Subclasses should override this method."""

        raise NotImplementedError()

    def get_image(self, name, size):
        """Get image by the name and size.

        [NOTE]: If there are many sizes of one image in the game, this method may be slow. To fix it.
        """

        if (name, size) in self.images:
            return self.images[name, size]

        image = load_image([get_data_path(self.name), name], size)
        self.images[name, size] = image
        return image

    def get_font(self, name, size):
        """Get font by the name and size, such as get_image."""

        if (name, size) in self.fonts:
            return self.fonts[name, size]

        font = pygame.font.Font(name, size)
        self.fonts[name, size] = font

        return font
