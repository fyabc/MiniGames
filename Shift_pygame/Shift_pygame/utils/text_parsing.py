# -*- coding: utf-8 -*-

import re

__author__ = 'fyabc'

_comment_pattern = re.compile(r'#.*?\n')
_atom_pattern = re.compile(r'\S+|(?:\".*?\")|(?:\'.*?\')')


def strip_line(line):
    """Remove comments (Start with '#') from the line."""

    return _comment_pattern.sub('', line).strip()


def next_line(f_it):
    while True:
        line = strip_line(next(f_it))
        if line:
            return line


def split_command(line):
    return _atom_pattern.findall(line)