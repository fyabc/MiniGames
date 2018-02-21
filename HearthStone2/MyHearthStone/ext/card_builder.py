#! /usr/bin/python
# -*- coding: utf-8 -*-

"""Card builder tools.

Interpret **HearthStone Design Language (HDL)** code to Python classes.
"""

__author__ = 'fyabc'


def load_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return load_string(f.read())


def load_string(string):
    # todo
    return None


__all__ = [
    'load_file',
    'load_string',
]
