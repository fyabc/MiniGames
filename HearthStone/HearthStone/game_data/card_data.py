#! /usr/bin/python
# -*- coding: utf-8 -*-

import os
from collections import defaultdict

from ..game_entities.card import Card, SetDataMeta
from ..utils import LoadCardPath, get_module_vars

__author__ = 'fyabc'


# Card data.
AllCards = {}
AllPackages = defaultdict(set)


def load_all_cards():
    for data_path in LoadCardPath:
        if not os.path.exists(data_path):
            continue
        for name in os.listdir(data_path):
            if name.endswith('.py'):
                module_vars = get_module_vars(os.path.join(data_path, name))
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
