#! /usr/bin/python
# -*- encoding: utf-8 -*-

from random import choice

from ..game_data.card_data import get_all_cards

__author__ = 'fyabc'


_filter_result_cache = {}


class Conditions:
    def __init__(self, *condition_strings, **conditions):
        pass

    def to_sorted_tuple(self):
        pass

    def __hash__(self):
        pass


def filter_cards(*condition_strings, **condition_pairs):
    """Filter, cache and return the set of cards id that satisfy the conditions.

    :param condition_pairs: key-value pair of conditions.
    :return: A set of cards that
    """

    global _filter_result_cache

    conditions = Conditions(*condition_strings, **condition_pairs)

    if conditions in _filter_result_cache:
        return _filter_result_cache[conditions]

    pass
