#! /usr/bin/python
# -*- encoding: utf-8 -*-

"""A simple compiler of card definition language, using PLY.

Example:
    Minion 侏儒发明家 {        # Define a new minion
        {% id = 0, name = '侏儒发明家', type = 0, CAH = [4, 2, 4], klass = 0 %}
        bc { d 1 }
        dr { d 1 }
    }
"""

import re
from types import new_class
from collections import namedtuple

from ply.lex import lex
from ply.yacc import yacc

from ..game_entities.card import Minion, Spell, Weapon

__author__ = 'fyabc'


#########
# Lexer #
#########

# Reserved words.
ReservedWords = {
    'Minion': ('CARD_TYPE', Minion),
    'Spell': ('CARD_TYPE', Spell),
    'Weapon': ('CARD_TYPE', Weapon),

    'bc': ('SKILL', 'battle_cry'),
    'battle_cry': ('SKILL', None),
    'dr': ('SKILL', 'death_rattle'),
    'death_rattle': ('SKILL', None),
    'play': ('SKILL', None),

    'def': ('DEF', None),
}

# Token list.
tokens = ['DICT', 'LINE_CODE', 'NUM', 'ID', 'CARD_TYPE', 'SKILL', 'DEF']

# Literals list.
literals = ['{', '}', '(', ')']

# Ignored characters.
t_ignore = ' \t\r\n'

# Token specifications (as Regex).


# Token processing functions.
def t_DICT(t):
    r"""\{%.*?%}"""

    t.value = eval('dict({})'.format(t.value[2:-2]))
    return t


def t_LINE_CODE(t):
    r"""\$.*?\n"""

    t.value = t.value[1:].strip()
    return t


def t_NUM(t):
    r"""\d+"""
    t.value = int(t.value)
    return t


def t_ID(t):
    # r"""[a-zA-Z_][a-zA-Z_0-9]*"""
    r"""[^\W0-9]\w*"""
    token = ReservedWords.get(t.value, ('ID', None))

    t.type = token[0]
    if token[1] is not None:
        t.value = token[1]

    return t


def t_COMMENT(t):
    r"""\#.*"""
    pass


# Error handler.
def t_error(t):
    print('Bad character: {!r}'.format(t.value[0]))
    t.lexer.skip(1)


# Build the lexer
lexer = lex(reflags=re.UNICODE)


##########
# Parser #
##########


Action = namedtuple('Action', ['type', 'value'])


def p_card(p):
    """card : CARD_TYPE ID '{' card_contents '}'
            | CARD_TYPE '{' card_contents '}'
    """

    if len(p) == 5:
        cls_name = ''
        cls_dict = p[3]
    else:
        cls_name = p[2]
        cls_dict = p[4]

    p[0] = new_class(cls_name, (p[1],), {}, lambda ns: ns.update(cls_dict))


def p_card_contents(p):
    """card_contents : empty
                     | card_contents content_entry
    """

    if len(p) == 2:
        p[0] = {}
    else:
        p[0] = p[1]

        k, v = p[2]
        p[0][k] = v


def p_content_entry(p):
    """content_entry : data_definition
                     | skill_definition
                     | func_definition
    """

    p[0] = p[1]


def p_data_definition(p):
    """data_definition : DICT"""
    p[0] = '_data', p[1]


def p_func_definition(p):
    """func_definition : DEF ID '(' ')' '{' statements '}'"""

    exec('''\
def __func_do_not_override_this_name(self):
    {}
    pass
'''.format('\n    '.join(s.value for s in p[6])), {}, get_skill_locals())

    p[0] = p[2], get_skill_locals().pop('__func_do_not_override_this_name')


def p_statements(p):
    """statements : empty
                  | statements statement
    """

    if len(p) == 2:
        p[0] = []
    else:
        p[0] = p[1]
        p[0].append(p[2])


def p_statement(p):
    """statement : LINE_CODE"""

    p[0] = Action('statement', p[1])


def p_skill_definition(p):
    """skill_definition : SKILL '{' actions '}'"""

    # Parse skills.
    if p[1] == 'battle_cry':
        skill_name = 'run_battle_cry'
        args_string = 'self, player_id, index'
    elif p[1] == 'death_rattle':
        skill_name = 'run_death_rattle'
        args_string = 'self, player_id, index'
    elif p[1] == 'play':
        skill_name = 'play'
        args_string = 'self, player_id, target'
    else:
        skill_name = p[1]
        args_string = 'self'

    result_statements = []
    for action in p[3]:
        if action.type == 'statement':
            result_statements.append(action.value)
        else:
            # todo: add more actions
            pass

    exec('''\
def __skill_do_not_override_this_name({}):
    {}
    pass
'''.format(args_string, '\n    '.join(result_statements)), {}, get_skill_locals())

    p[0] = skill_name, get_skill_locals().pop('__skill_do_not_override_this_name')


def p_actions(p):
    """actions : empty
               | actions action
    """

    if len(p) == 2:
        p[0] = []
    else:
        p[0] = p[1]
        p[0].append(p[2])


def p_action(p):
    """action : statement"""

    p[0] = p[1]


def p_empty(p):
    """empty :"""
    pass


# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input {}!".format(p))


_default_locals = None


def get_skill_locals():
    global _default_locals
    if _default_locals is None:
        from HearthStone.ext import Minion, Spell, Weapon, set_description
        from HearthStone.ext.card_creator import m_blank, w_blank, m_summon
        from HearthStone.ext.card_creator import validator_minion, validator_enemy_minion
        from HearthStone.ext.card_creator import action_damage, action_destroy
        from HearthStone.ext import DrawCard, AddCardToHand
        from HearthStone.ext import Damage, SpellDamage, RestoreHealth, GetArmor
        from HearthStone.ext import RandomTargetDamage
        from HearthStone.ext import GameHandler, DeskHandler, FreezeOnDamage
        from HearthStone.ext import AddMinionToDesk
        from HearthStone.ext import TurnBegin
        from HearthStone.ext import MinionDeath
        from HearthStone.ext import constants
        from HearthStone.utils.debug_utils import verbose

        _default_locals = locals()
    return _default_locals


# Build the parser
parser = yacc()

parse_card = parser.parse


__all__ = [
    'lexer',
    'parser',
    'parse_card',
]
