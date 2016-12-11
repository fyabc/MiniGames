#! /usr/bin/python
# -*- coding: utf-8 -*-

from collections import defaultdict

from ..game_entities.card import Card, SetDataMeta
from ..utils import LoadDataPath, CardPackageName, get_module_vars

__author__ = 'fyabc'


# Card data.
AllCards = None
AllPackages = defaultdict(set)


def get_all_cards():
    global AllCards

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

    return AllCards


__all__ = [
    'AllCards',
    'get_all_cards',
]
