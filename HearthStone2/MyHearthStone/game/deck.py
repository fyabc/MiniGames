#! /usr/bin/python
# -*- coding: utf-8 -*-

"""The deck class and related utilities."""

import base64
import binascii

from ..utils.message import error

__author__ = 'fyabc'


class Deck:
    """The class of a deck.

    This class is usually used for deck I/O.
    """

    AllModes = ['standard', 'wild', 'arena', '乱斗']

    def __init__(self, hero_id, card_id_list, mode='standard', **kwargs):
        self.mode = mode
        self.hero_id = hero_id
        self.card_id_list = card_id_list

    def __repr__(self):
        return 'Deck(mode={}, hero_id={}, card_id_list={})'.format(self.mode, self.hero_id, self.card_id_list)

    def to_code(self, comment=True):
        """Convert deck to code.

        :param comment: Add comment into generated code.
        :return: code: A string of deck.
        """

        str_deck = '{} {} {}'.format(self.mode, self.hero_id, ' '.join(str(e) for e in self.card_id_list))

        result = base64.b64encode(str_deck.encode('ascii')).decode('ascii')

        if comment:
            pass
            # todo

        return result

    @classmethod
    def from_code(cls, code):
        """Convert deck from code.

        :param code: A string of deck.
        :return: A ``Deck`` instance.
        """

        lines = code.split('\n')
        code_line = ''
        for line in lines:
            # Get the first line not start with comment ('#')
            if not line.startswith('#'):
                code_line = line
                break

        try:
            str_deck = base64.b64decode(code_line).decode('ascii')

            mode, hero_id, *card_id_list = str_deck.split()

            if mode not in cls.AllModes:
                error('Unknown deck mode, return None')
                return None

            hero_id = int(hero_id)
            card_id_list = [int(e) for e in card_id_list]

            return cls(hero_id, card_id_list, mode)
        except binascii.Error as e:
            error(e)
            error('Error when loading deck code, return None')
            return None
        except ValueError:
            error('Error when loading deck code, return None')
            return None
