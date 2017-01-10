#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'fyabc'


def sign(x):
    return 1 if x > 0 else (-1 if x < 0 else 1)


__all__ = [
    'sign',
]
