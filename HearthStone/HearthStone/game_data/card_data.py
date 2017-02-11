#! /usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3

from ..game_entities.card import Card, SetDataMeta
from ..utils.path_utils import LoadDataPath, CardPackageName
from ..utils.basic_utils import get_module_vars
from ..constants import race2str, str2race

__author__ = 'fyabc'


# Card data.
AllCards = None

AllCardsDB = None
AllCardsDBCur = None


def _create_cards_db():
    global AllCards, AllCardsDB, AllCardsDBCur

    assert AllCards is not None, 'AllCards must not be None'

    AllCardsDB = sqlite3.connect(':memory:')
    AllCardsDBCur = AllCardsDB.cursor()

    AllCardsDBCur.execute('''\
    CREATE TABLE AllCards (
      id            INTEGER PRIMARY KEY NOT NULL,
      type          INTEGER,
      name          VARCHAR(255),
      package       INTEGER,
      rarity        INTEGER,
      klass         INTEGER,
      race          VARCHAR(40),
      cost          INTEGER,
      attack        INTEGER NULLABLE,
      health        INTEGER NULLABLE,
      overload      INTEGER,
      spell_power   INTEGER,
      attack_number INTEGER NULLABLE,
      taunt         INTEGER NULLABLE,
      charge        INTEGER NULLABLE,
      divine_shield INTEGER NULLABLE,
      stealth       INTEGER NULLABLE
    );
    ''')

    AllCardsDBCur.executemany(
        '''INSERT INTO AllCards VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);''',
        ((
            card.data['id'],
            card.data['type'],
            card.data['name'],
            card.data['package'],
            card.data['rarity'],
            card.data['klass'],
            race2str(card.data['race']),
            card.data['CAH'][0],
            card.data['CAH'][1] if len(card.data['CAH']) >= 2 else None,
            card.data['CAH'][2] if len(card.data['CAH']) >= 3 else None,
            card.data['overload'],
            card.data['spell_power'],
            card.data.get('attack_number', None),
            card.data.get('taunt', None),
            card.data.get('charge', None),
            card.data.get('divine_shield', None),
            card.data.get('stealth', None),
         ) for card in AllCards.values())
    )


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

    _create_cards_db()

    return AllCards


def get_cards_db():
    global AllCardsDB

    if AllCardsDB is None:
        get_all_cards()

    return AllCardsDB


def get_card_type(id_or_name):
    if isinstance(id_or_name, int):
        return get_all_cards()[id_or_name]
    elif isinstance(id_or_name, str):
        cursor = get_cards_db().cursor()
        cursor.execute('''SELECT id FROM AllCards WHERE (name = ?)''', (id_or_name,))
        result = cursor.fetchall()
        result_id = result[0][0]
        return get_all_cards()[result_id]
    else:
        raise TypeError('id_or_name must be int or string')


__all__ = [
    'get_all_cards',
    'get_cards_db',
]
