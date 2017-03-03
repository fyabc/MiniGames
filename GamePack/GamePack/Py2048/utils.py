#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'fyabc'


def fill_list(l, length, fill_value=-1, left=True):
    fill = [fill_value for _ in range(length - len(l))]

    if left:
        return l + fill
    else:
        return fill + l
