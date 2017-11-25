#! /usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import cmd
import shlex

from ...game.core import Game
from ...game.deck import Deck
from ..frontend import Frontend
from ...utils.constants import C
from ...utils.game import Klass
from ...utils.message import error, note

__author__ = 'fyabc'


class ParserExit(Exception):
    """The exception for the exit of the parser (both normal exit and error)."""


class NoExitParser(argparse.ArgumentParser):
    def exit(self, status=0, message=None):
        if message:
            print(message, end='' if message.endswith('\n') else '\n')
        raise ParserExit(status, message)


class TextSingleSession(cmd.Cmd):
    intro = '''\
{}
Welcome to HearthStone (single player text mode).
'''.format('HearthStone'.center(C.Logging.Width, '='))

    StateMain = 'main'
    StateGame = 'game'

    prompt_pattern = 'HS[{}]{}> '

    def __init__(self, frontend: Frontend):
        super().__init__()
        self.frontend = frontend
        self.state = self.StateMain

        # Command parsers.
        self.parser_user = NoExitParser(add_help=True, prog='user')
        self.sub_user = self.parser_user.add_subparsers(dest='action')
        self.sub_user.default = 'show'
        parser_user_show = self.sub_user.add_parser('show')
        parser_user_all = self.sub_user.add_parser('all')
        parser_user_name = self.sub_user.add_parser('name')
        parser_user_name.add_argument('new_name', nargs='?', default=None, help='New name, default is None')

        self.parser_deck = NoExitParser(add_help=True, prog='deck')
        self.sub_deck = self.parser_deck.add_subparsers(dest='action')
        self.sub_deck.default = 'list'
        parser_deck_list = self.sub_deck.add_parser('list')
        parser_deck_new = self.sub_deck.add_parser('new')
        parser_deck_new.add_argument('-c', '--class', action='store', dest='klass', default=None,
                                     help='Deck class (str or int), default is None')
        parser_deck_new.add_argument('-n', '--name', action='store', dest='name', default=None,
                                     help='Deck name, default is None')
        parser_deck_delete = self.sub_deck.add_parser('delete')
        delete_group = parser_deck_delete.add_mutually_exclusive_group(required=True)
        delete_group.add_argument('index', nargs='?', default=None, type=int, help='Delete by index')
        delete_group.add_argument('-n', '--name', action='store', dest='index', default=None,
                                        help='Delete by name, default is None')
        parser_deck_show = self.sub_deck.add_parser('show')

    def emptyline(self):
        pass

    def preloop(self):
        if self.frontend.game.running:
            player_str = '(P{})'.format(self.frontend.game.current_player)
        else:
            player_str = ''
        self.prompt = self.prompt_pattern.format(self.state, player_str)

    @staticmethod
    def do_quit(arg):
        """\
Terminate the application.
Syntax: q | quit | exit\
"""
        return True

    do_exit = do_q = do_quit

    def do_user(self, arg):
        try:
            args = self.parser_user.parse_args(shlex.split(arg))
        except ParserExit:
            return

        user = self.frontend.user
        if args.action == 'show':
            print(user)
        elif args.action == 'all':
            user_list = user.get_user_list()
            if user_list is None:
                user_list = []
            user_ids = [e[0] for e in user_list]
            try:
                index = user_ids.index(user.user_id)
                user_list[index][1] = user.nickname
            except ValueError:
                user_list.insert(0, [user.user_id, user.nickname])

            print('All users:')
            for i, n in user_list:
                print('{} {}\t{}'.format(('*' if i == user.user_id else ' '), i, n))
            print('=========')
        elif args.action == 'name':
            if args.new_name is not None:
                old_name = user.nickname
                user.nickname = args.new_name
                print('Name "{}" -> "{}"'.format(old_name, user.nickname))
            else:
                print('Name: "{}"'.format(user.nickname))

    def complete_user(self, *args):
        return [c for c in self.sub_user.choices if c.startswith(args[0])]

    def do_deck(self, arg):
        try:
            args = self.parser_deck.parse_args(shlex.split(arg))
        except ParserExit:
            return

        decks = self.frontend.user.decks
        if args.action == 'list':
            print('My Decks:')
            for i, deck in enumerate(decks):
                print(i, '\t', deck, sep='')
            print('=========')
        elif args.action == 'new':
            while True:
                if args.klass is not None:
                    klass = args.klass
                else:
                    klass = input('> Choose class [0-10 or name]:')
                try:
                    _klass = Klass.Str2Idx.get(klass.capitalize(), None)
                    if _klass is not None:
                        klass = _klass
                        break
                    klass = int(klass)
                    if not 0 <= klass <= 10:
                        raise ValueError
                    break
                except ValueError:
                    error('Please enter number [0-10] or name.')
            klass_name = Klass.Idx2Str[klass]
            if args.name is not None:
                name = args.name
            else:
                name = input('> Enter deck name ["Custom {}"]:'.format(klass_name))
            if not name:
                name = 'Custom {}'.format(klass_name)
            # TODO
            decks.append(Deck(klass=klass, card_id_list=[], name=name))
            note('Create new deck: {}[{}]'.format(name, klass_name))
        elif args.action == 'delete':
            if isinstance(args.index, str):
                try:
                    index = ([d.name for d in decks]).index(args.index)
                except ValueError:
                    error('Cannot find deck {!r}.'.format(args.index))
                    return
            else:
                if not 0 <= args.index < len(decks):
                    error('Index out of range.')
                    return
                index = args.index
            while True:
                confirm = input('> Delete deck {} {}, confirm? (y/n) '.format(index, decks[index])).lower()
                if confirm == 'y':
                    note('Deck {} {} deleted.'.format(index, decks[index]))
                    del decks[index]
                    return
                elif confirm == 'n':
                    note('Nothing happens.')
                    return
                else:
                    pass

    def complete_deck(self, *args):
        return [c for c in self.sub_deck.choices if c.startswith(args[0])]

    def do_game(self, arg):
        """\
Start a new game.
Syntax: game deck-file1 deck-file2 [mode=standard]\
"""

        args = shlex.split(arg)
        print(args)

    def do_draw(self, arg):
        import turtle as t
        t.tracer(False)
        t.color('red', 'yellow')
        # t.speed(10)
        t.begin_fill()
        for _ in range(50):
            t.forward(200)
            t.left(170)
        t.end_fill()

        t.done()


class TextSingleFrontend(Frontend):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.game = Game(frontend=self)
        self.session = TextSingleSession(self)

    def _main(self):
        self.session.cmdloop()

    def run(self):
        pass

    def _draw_status(self):
        pass


__all__ = [
    'TextSingleFrontend',
]
