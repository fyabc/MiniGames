#! /usr/bin/python
# -*- coding: utf-8 -*-

from collections import Mapping

__author__ = 'fyabc'


class DynamicObject:
    def __init__(self, *args, **kwargs):
        for arg in args:
            if isinstance(arg, Mapping):
                for k, v in arg.items():
                    setattr(self, k, v)
            else:
                raise TypeError('arguments must be mapping objects')

        for k, v in kwargs.items():
            setattr(self, k, v)

    def __str__(self):
        return '({})'.format(','.join('{}={}'.format(k, v) for k, v in self.__dict__.items()))
