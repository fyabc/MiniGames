#! /usr/bin/python
# -*- encoding: utf-8 -*-

"""A simple compiler of card definition language, using PLY.

Example:
    Minion {        # Define a new minion
        data {% %}
        bc { d 1 }
        dr { d 1 }
    }
"""

from ply.lex import lex
from ply.yacc import yacc

from HearthStone.game_entities.card import Minion, Spell, Weapon

__author__ = 'fyabc'


#########
# Lexer #
#########

# Reserved words.
ReservedWords = {
    'Minion': 'CARD_TYPE',
    'Spell': 'CARD_TYPE',
    'Weapon': 'CARD_TYPE',
}

# Token list.
tokens = ['DICT', 'NUM', 'LP', 'RP', 'CARD_TYPE', 'ID']

# Ignored characters.
t_ignore = ' \t\r\n'

# Token specifications (as Regex).
t_DICT = r'\{%.*?%}'
t_LP = r'\{'
t_RP = r'}'


# Token processing functions.
def t_NUM(t):
    r"""\d+"""
    t.value = int(t.value)
    return t


def t_ID(t):
    r"""[a-zA-Z_][a-zA-Z_0-9]*"""
    t.type = ReservedWords.get(t.value, 'ID')
    return t


def t_COMMENT(t):
    r"""\#.*"""
    pass


# Error handler.
def t_error(t):
    print('Bad character: {!r}'.format(t.value[0]))
    t.skip(1)


# Build the lexer
lexer = lex()


##########
# Parser #
##########


__all__ = [
    'lexer',
]
