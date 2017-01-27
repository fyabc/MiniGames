#! /usr/bin/python
# -*- coding: utf-8 -*-

import re
import sys

__author__ = 'fyabc'


def error(msg, *args, **kwargs):
    print(msg, *args, **kwargs, file=sys.stderr)


def sign(x):
    return 1 if x > 0 else (-1 if x < 0 else 1)


_comment_pattern = re.compile(r'#.*?\n')


def strip_line(line):
    """Remove comments (Start with '#') from the line."""

    return _comment_pattern.sub('', line).strip()


def lget(l, i, default=None):
    """Get the i-th element of the list l. If not exist, return the default value."""

    try:
        return l[i]
    except IndexError:
        return default
