#! /usr/bin/python
# -*- encoding: utf-8 -*-

from random import choice

from ..game_data.card_data import get_all_cards, get_cards_db

__author__ = 'fyabc'


_query_result_cache = {}


class Conditions:
    default_conditions = [
        'rarity <> -1',
    ]

    def __init__(self, *condition_strings):
        self.conditions = sorted(self.default_conditions + list(condition_strings))

    def to_sorted_tuple(self):
        pass

    def __hash__(self):
        return hash(tuple(self.conditions))

    def __eq__(self, other):
        return self.conditions == other.conditions


def _query_cards(cur, cond):
    cur.execute('''SELECT id FROM AllCards {}'''.format(
        'WHERE ({})'.format(
            'AND'.join(
                '({})'.format(condition)
                for condition in cond.conditions
            )
        ) if cond.conditions
        else ''
    ))

    result = cur.fetchall()

    return [row[0] for row in result]


def filter_cards(*condition_strings):
    """Filter, cache and return the set of cards id that satisfy the conditions.

    :param condition_strings: strings of conditions, must be SQL statements.
        Example: rarity <> -1; type = 0; ...
    :return: A set of cards that satisfy these conditions.
    """

    global _query_result_cache

    conditions = Conditions(*condition_strings)

    if conditions in _query_result_cache:
        return _query_result_cache[conditions]

    result = _query_cards(get_cards_db().cursor(), conditions)
    _query_result_cache[conditions] = result

    return result


def random_card(*condition_strings):
    candidates = filter_cards(*condition_strings)

    if candidates:
        return choice(candidates)
    else:
        return None


__all__ = [
    'filter_cards',
    'random_card',
]
