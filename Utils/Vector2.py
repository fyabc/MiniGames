# -*- coding: utf-8 -*-

from math import sqrt

__author__ = 'fyabc'


class Vector2:
    __slots__ = ('_v', )

    def __init__(self, x=0., y=0.):
        if hasattr(x, '__getitem__'):
            x, y = x
        self._v = [x, y]

    def __str__(self):
        x, y = self._v
        return '(%f, %f)' % (x, y)

    @property
    def length(self):
        """Length of the vector."""
        x, y = self._v
        return sqrt(x * x + y * y)

    @length.setter
    def length(self, newLength):
        v = self._v
        try:
            l = newLength / self.length
        except ZeroDivisionError:
            v[0], v[1] = 0.0, 0.0
            return
        v[0] *= l
        v[1] *= l


def test():
    v = Vector2(3, 5)
    print(v)
    print(v.length)
    v.length = 4
    print(v.length)
    print(v)


if __name__ == '__main__':
    test()
