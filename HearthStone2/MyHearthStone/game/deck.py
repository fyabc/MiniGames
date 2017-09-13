#! /usr/bin/python
# -*- coding: utf-8 -*-

"""The deck class and related utilities."""

__author__ = 'fyabc'


class Deck:
    """The class of a deck.

    This class is usually used for deck I/O.
    """

    def __init__(self, hero_id, card_id_list, mode='standard', **kwargs):
        self.mode = mode
        self.hero_id = hero_id
        self.card_id_list = card_id_list

    def to_code(self, comment=True):
        """Convert deck to code.

        :param comment: Add comment into generated code.
        :return: code: A string of deck.
        """

        # todo

        return ''

    @classmethod
    def from_code(cls, code):
        """Convert deck from code.

        :param code: A string of deck.
        :return: A ``Deck`` instance.
        """

        # todo
