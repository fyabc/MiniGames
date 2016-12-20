#! /usr/bin/python
# -*- encoding: utf-8 -*-

from HearthStone.ext.card_compiler import lexer

__author__ = 'fyabc'


def _test_lexer():
    string = '''\
    Minion {        # Define a new minion
        data {% id = 0, name = '侏儒发明家', type = 0, CAH = [4, 2, 4], klass = 0 %}
        bc { d 1 }
        dr { d 1 }
    }
'''
    lexer.input(string)

    for token in lexer:
        # type, value, lineno, lexpos
        print(token)


def _test_parser():
    pass


def _test():
    _test_lexer()


if __name__ == '__main__':
    _test()

