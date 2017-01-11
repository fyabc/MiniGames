#! /usr/bin/python
# -*- coding: utf-8 -*-

import sys

__author__ = 'fyabc'


def error(msg, *args, **kwargs):
    print(msg, *args, **kwargs, file=sys.stderr)


def sign(x):
    return 1 if x > 0 else (-1 if x < 0 else 1)
