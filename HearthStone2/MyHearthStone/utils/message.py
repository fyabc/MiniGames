#! /usr/bin/python
# -*- coding: utf-8 -*-

"""Utilities for output message."""

# TODO: Add logging file into it (using `logging` module)

from time import time as _time
from functools import partial as _partial
from contextlib import contextmanager as _cm

__author__ = 'fyabc'

# Debug levels.
LEVEL_DEBUG = 0
LEVEL_VERBOSE = 1
LEVEL_INFO = 2
LEVEL_COMMON = 2.5
LEVEL_WARNING = 3
LEVEL_ERROR = 4

_debug_level = LEVEL_COMMON


def set_debug_level(new_level):
    global _debug_level
    _debug_level = new_level


def get_debug_level():
    return _debug_level


def message(*args, **kwargs):
    level = kwargs.pop('level', LEVEL_INFO)
    if level >= _debug_level:
        print(*args, **kwargs)


debug = _partial(message, level=LEVEL_DEBUG)
verbose = _partial(message, level=LEVEL_VERBOSE)
info = _partial(message, level=LEVEL_INFO)
warning = _partial(message, level=LEVEL_WARNING)
error = _partial(message, level=LEVEL_ERROR)


@_cm
def msg_block(msg, level=LEVEL_INFO, log_time=True):
    if log_time:
        start_time = _time()
    message('{}... '.format(msg), end='', level=level)
    yield
    message('Done{}'.format(', time: {:.4f}s'.format(_time() - start_time) if log_time else ''), level=level)


def entity_message(self, kwargs, prefix=''):
    return '{}{}({})'.format(
        prefix,
        self.__class__.__name__,
        ', '.join(
            '{}={}'.format(k, v)
            for k, v in kwargs.items()
        )
    )
