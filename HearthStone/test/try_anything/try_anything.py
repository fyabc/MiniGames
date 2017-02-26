#! /usr/bin/python
# -*- coding: utf-8 -*-

"""This file is used to try or test some small things."""

__author__ = 'fyabc'


def _test():
    from HearthStone.game_data.card_data import AllCards

    for card_id, card_type in AllCards.items():
        print(card_id)
        print(card_type.__mro__)
        print(card_type.data)
        print()


if __name__ == '__main__':
    _test()
