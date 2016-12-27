#! /usr/bin/python
# -*- encoding: utf-8 -*-

from HearthStone.ext.card_compiler import lexer, parse_card

__author__ = 'fyabc'


TestString = '''\
    Minion 侏儒发明家 {        # Define a new minion
        {% id = 0, name = '侏儒发明家', type = 0, CAH = [4, 2, 4], klass = 0 %}
        bc {
            $ self.game.add_event_quick(DrawCard, self.player_id, self.player_id)
        }

        dr {
        }

        def func() {
            $ print(3)
        }
    }
'''


def _test_lexer():
    lexer.input(TestString)

    for token in lexer:
        # type, value, lineno, lexpos
        print(token)


def _test_parser():
    result = parse_card(TestString)

    print(result)
    print(result.__name__)
    print(result.data)
    result.func(self=None)


def _test():
    _test_lexer()

    print()

    _test_parser()
    pass


if __name__ == '__main__':
    _test()
