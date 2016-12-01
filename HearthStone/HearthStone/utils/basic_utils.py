#! /usr/bin/python
# -*- encoding: utf-8 -*-

__author__ = 'fyabc'


def cls_name(obj):
    if isinstance(obj, type):
        return obj.__name__
    else:
        return obj.__class__.__name


__all__ = [
    'cls_name',
]
