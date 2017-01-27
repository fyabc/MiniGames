#! /usr/bin/python
# -*- coding: utf-8 -*-

import sys

__author__ = 'fyabc'


def error(msg, *args, **kwargs):
    print(msg, *args, **kwargs, file=sys.stderr)


def sign(x):
    return 1 if x > 0 else (-1 if x < 0 else 1)


def lget(l, i, default=None):
    """Get the i-th element of the list l. If not exist, return the default value."""

    try:
        return l[i]
    except IndexError:
        return default
