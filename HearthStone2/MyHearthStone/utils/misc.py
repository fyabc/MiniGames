#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'fyabc'


def trivial_impl(func):
    """Decorator that mark this function is a trivial implementation. Used for subclasses.

    Example::

        class B:
            @trivial_impl
            def f(self):
                pass

        class C(B):
            def f(self):
                pass

        is_trivial_impl(B.f)    # True
        is_trivial_impl(B().f)  # True
        is_trivial_impl(C.f)    # False
        is_trivial_impl(C().f)  # False
    """
    setattr(func, '__is_trivial_impl', True)
    return func


def is_trivial_impl(func):
    return bool(getattr(func, '__is_trivial_impl', False))


__all__ = [
    'trivial_impl',
    'is_trivial_impl',
]
