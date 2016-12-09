#! /usr/bin/python
# -*- encoding: utf-8 -*-

__author__ = 'fyabc'


def cls_name(obj):
    if isinstance(obj, type):
        return obj.__name__
    else:
        return obj.__class__.__name


def get_module_vars(_file_name):
    with open(_file_name, 'r', encoding='utf-8') as _f:
        exec(_f.read())

        return vars()


__all__ = [
    'cls_name',
    'get_module_vars',
]
