#! /usr/bin/python
# -*- encoding: utf-8 -*-

from collections import defaultdict

import pygame.locals

from ..config import KeymapPath
from .text_parsing import strip_line

__author__ = 'fyabc'

_keymap = None


def get_keymap():
    global _keymap

    if _keymap is None:
        _keymap = defaultdict(set)

        with open(KeymapPath, 'r') as keymap_file:
            for line in keymap_file:
                words = strip_line(line).split()

                if len(words) < 2:
                    continue

                _keymap[words[0]].add(pygame.locals.__dict__['K_' + words[1]])
    return _keymap


def get_unique_key_event(key_name, is_down=True):
    if is_down:
        event_type = pygame.locals.KEYDOWN
    else:
        event_type = pygame.locals.KEYUP

    if isinstance(key_name, str):
        key_name = eval('pygame.locals.{}'.format(key_name))
    return event_type, key_name


def get_unique_mouse_event(mouse_id, is_down=True):
    if is_down:
        event_type = pygame.locals.MOUSEBUTTONDOWN
    else:
        event_type = pygame.locals.MOUSEBUTTONUP
    return event_type, mouse_id
