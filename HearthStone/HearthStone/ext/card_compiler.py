#! /usr/bin/python
# -*- coding: utf-8 -*-

"""Create cards with a simple language.

This is a simple compiler of the card.

The simple card definition language (still designing...):

    {
        data { id = 0, type = 0, name = '侏儒发明家', CAH = [4, 2, 4], klass = 0 }
        bc { d 1 }
        dr { d 1 }
    }
"""

from collections import namedtuple
import re

__author__ = 'fyabc'


# Tokens.
T_LP = r'(?P<T_LP>\{)'
T_RP = r'(?P<T_RP>})'
T_NUM = r'(?P<T_NUM>\d+)'
T_ID = r'(?P<T_ID>[a-zA-Z_][a-zA-Z_0-9]*)'
T_WS = r'(?P<T_WS>\s+)'


MasterPattern = re.compile('|'.join([T_LP, T_RP, T_NUM, T_ID, T_WS]))


def tokenizer(string, pattern=MasterPattern, skips=('T_WS',)):
    Token = namedtuple('Token', ['type', 'value'])

    scanner = pattern.scanner(string)

    for m in iter(scanner.match, None):
        token = Token(m.lastgroup, m.group())
        if token.type in skips:
            continue
        yield token


def create_card_from_string(card_string):
    pass


def _test():
    for tok in tokenizer('''
{
    bc { d 1 }
    dr { d 1 }
}
'''):
        print(tok)


if __name__ == '__main__':
    _test()

