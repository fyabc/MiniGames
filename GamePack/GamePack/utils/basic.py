#! /usr/bin/python
# -*- encoding: utf-8 -*-

import os

import pygame

__author__ = 'fyabc'


def get_key_name(key, keymap):
    for key_name, keys in keymap.items():
        if key in keys:
            return key_name
    return None


def parse_size(string):
    """Parse the size string into integers.

    The size string must in the format of 'axb', a and b are positive integers.

    :param string: The input string.
    :return: A pair of 2 integers: (row, column)
    :raise: ValueError
    """

    parts = string.split('x')

    if len(parts) < 2:
        raise ValueError('At least 1 separator required')

    row, column = parts[0], parts[1]

    try:
        row = int(row)
        column = int(column)
    except ValueError:
        raise

    return row, column


def load_image(path_list, size=None):
    image = pygame.image.load(os.path.join(*path_list)).convert_alpha()

    if size is not None:
        image = pygame.transform.scale(image, size)

    return image
