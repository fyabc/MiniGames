#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'fyabc'


def order_of_play(objects):
    """Sort objects by the order of play.

    :param objects: Entities or events or triggers.
    :return: List of objects, sorted by order of play.
    """

    return sorted(objects, key=lambda o: o.oop)


__all__ = [
    'order_of_play',
]
