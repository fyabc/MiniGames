#! /usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3

from ..game_entities.card import Card, SetDataMeta
from ..utils import LoadDataPath, CardPackageName, get_module_vars

__author__ = 'fyabc'


# Card data.
AllCards = None

AllCardsDB = None
AllCardsDBCur = None


def get_all_cards():
    global AllCards, AllCardsDB, AllCardsDBCur

    if AllCards is not None:
        return AllCards

    AllCards = {}

    for module_vars in get_module_vars(LoadDataPath, CardPackageName):
        for card_typename, card_type in module_vars.items():
            if type(card_type) == SetDataMeta and issubclass(card_type, Card):
                data = card_type.data

                card_id = data.get('id', None)
                if card_id is None:
                    continue

                if card_id in AllCards:
                    raise KeyError('The card id {} already exists'.format(card_id))

                AllCards[card_id] = card_type

    # todo: create cards db
    AllCardsDB = sqlite3.connect(':memory:')
    AllCardsDBCur = AllCardsDB.cursor()

    AllCardsDBCur.execute('''\
CREATE TABLE AllCards (
  id INTEGER PRIMARY KEY NOT NULL,
  type INTEGER(4)
);
''')

    return AllCards


def get_cards_db():
    global AllCardsDB

    if AllCardsDB is None:
        get_all_cards()

    return AllCardsDB


__all__ = [
    'get_all_cards',
    'get_cards_db',
]
