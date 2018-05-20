#! /usr/bin/python
# -*- coding: utf-8 -*-

"""The deck class and related utilities."""

import base64
import binascii

from ..utils.game import Klass
from ..utils.message import error, info

__author__ = 'fyabc'


class Deck:
    """The class of a deck.

    This class is usually used for deck I/O.
    """

    AllModes = ['standard', 'wild', 'arena', 'brawl']

    _delimiter = '\1'

    def __init__(self, klass, card_id_list, mode='standard', **kwargs):
        self.mode = mode
        self.klass = klass
        self.card_id_list = card_id_list
        self._name = kwargs.pop('name', 'Custom {}'.format(Klass.Idx2Str[klass]))

    def __repr__(self):
        return 'Deck(class={}, name={!r}, mode={})'.format(Klass.Idx2Str[self.klass], self.name, self.mode)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        info('Set name of {} to {}'.format(self, value))
        self._name = value

    def copy(self):
        """Return a (deep) copy of this deck."""

        return type(self)(self.klass, self.card_id_list[:], self.mode, name=self.name)

    def to_code(self, comment=True):
        """Convert deck to code.

        :param comment: Add comment into generated code.
        :return: code: A string of deck.
        """

        str_deck = '{}{}{}{}{}{}{}'.format(
            self.klass, self._delimiter,
            self.name, self._delimiter,
            self.mode, self._delimiter,
            self._delimiter.join(str(e) for e in self.card_id_list)
        )

        result = base64.b64encode(str_deck.encode('utf-8')).decode('ascii')

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
            str_deck = base64.b64decode(code_line).decode('utf-8')

            klass, name, mode, *card_id_list = str_deck.strip(cls._delimiter).split(cls._delimiter)

            if mode not in cls.AllModes:
                error('Unknown deck mode, return None')
                return None

            klass = int(klass)
            card_id_list = [str(e) for e in card_id_list]

            return cls(klass, card_id_list, mode, name=name)
        except binascii.Error as e:
            error(e)
            error('Error when loading deck code, return None')
            return None
        except ValueError as e:
            error(e)
            error('Error when loading deck code, return None')
            return None
