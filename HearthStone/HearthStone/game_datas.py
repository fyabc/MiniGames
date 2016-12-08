#! /usr/bin/python
# -*- coding: utf-8 -*-

import os

from .game_entities.card import Card, SetDataMeta
from .utils.path_utils import CardDataPath, UserCardDataPath, CardDataPackageName, UserCardDataPackageName

__author__ = 'fyabc'


# Card data.
AllCards = {}


def load_all_cards():
    for data_path, package_name in [
        (CardDataPath, CardDataPackageName),
        (UserCardDataPath, UserCardDataPackageName),
    ]:
        if not os.path.exists(data_path):
            continue
        for name in os.listdir(data_path):
            if name.endswith('.py'):
                module_name = name[:-3]
                exec('from {} import {}'.format(package_name, module_name))

                module_vars = eval('vars({})'.format(module_name))
                for card_typename, card_type in module_vars.items():
                    if type(card_type) == SetDataMeta and issubclass(card_type, Card):
                        data = card_type.data

                        card_id = data.get('id', None)
                        if card_id is None:
                            continue

                        if card_id in AllCards:
                            raise KeyError('The card id {} already exists'.format(card_id))

                        AllCards[card_id] = card_type


load_all_cards()


__all__ = [
    'AllCards',
]
