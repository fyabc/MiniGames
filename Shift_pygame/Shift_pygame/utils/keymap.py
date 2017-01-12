#! /usr/bin/python
# -*- encoding: utf-8 -*-

from collections import defaultdict

import pygame.locals

from ..config import KeymapPath
from ..utils.basic import strip_line

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
