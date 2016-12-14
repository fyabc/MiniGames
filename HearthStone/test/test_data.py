#! /usr/bin/python
# -*- coding: utf-8 -*-

import pprint

from HearthStone.game_data.card_data import get_cards_db, get_all_cards
from HearthStone.ext import filter_cards, random_card

__author__ = 'fyabc'


def get_id(cur, query):
    cur.execute(query)

    result = cur.fetchall()

    return [row[0] for row in result]


def print_id(cur, query):
    pprint.pprint(get_id(cur, query))


def _test_sql():
    db = get_cards_db()
    cur = db.cursor()

    print_id(cur, '''\
    SELECT id FROM AllCards
    WHERE (race LIKE '%3%' OR race LIKE '%1%')
    ''')

    print_id(cur, '''\
    SELECT id FROM AllCards
    WHERE ((cost % 2 = 1) AND (rarity <> -1))
    ''')


def _test_filters():
    all_cards = get_all_cards()

    pprint.pprint(filter_cards('cost = 7'))
    pprint.pprint(random_card('rarity = -1'))

    card0 = all_cards[0]
    print(card0.run_death_rattle)

    card4001 = all_cards[4001]
    print(card4001.run_death_rattle)


def _test():
    _test_filters()


if __name__ == '__main__':
    _test()

