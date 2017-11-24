#! /usr/bin/python
# -*- coding: utf-8 -*-

import cmd
import shlex

from ...game.core import Game
from ..frontend import Frontend
from ...utils.constants import C

__author__ = 'fyabc'


class TextSingleSession(cmd.Cmd):
    intro = '''\
{}
Welcome to HearthStone (single player text mode).
'''.format('HearthStone'.center(C.Logging.Width, '='))

    StateMain = 'main'
    StateGame = 'game'

    # TODO: add argparse into the parse of commands.

    def __init__(self, frontend: Frontend):
        super().__init__()
        self.prompt = 'HS[{}]{}> '
        self.frontend = frontend
        self.state = self.StateMain

    def emptyline(self):
        pass

    def preloop(self):
        if self.frontend.game.running:
            player_str = '(P{})'.format(self.frontend.game.current_player)
        else:
            player_str = ''
        self.prompt = self.prompt.format(self.state, player_str)

    @staticmethod
    def do_quit(arg):
        """\
Terminate the application.
Syntax: q | quit | exit\
"""
        return True

    do_exit = do_q = do_quit

    def do_user(self, arg):
        args = shlex.split(arg)
        user = self.frontend.user
        if not args:
            print(user)
        elif args[0] == 'all':
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
        elif args[0] == 'name':
            if len(args) >= 2:
                old_name = user.nickname
                user.nickname = args[1]
                print('Name "{}" -> "{}"'.format(old_name, user.nickname))
            else:
                print('Name: "{}"'.format(user.nickname))

    def complete_user(self, *args):
        all_commands = ['all', 'name']
        return [c for c in all_commands if c.startswith(args[0])]

    def do_deck(self, arg):
        args = shlex.split(arg)

        if not args:
            print('My Decks:')
            for deck in self.frontend.user.decks:
                print(deck)
            print('---------')

    def do_game(self, arg):
        """\
Start a new game.
Syntax: game deck-file1 deck-file2 [mode=standard]\
"""

        args = shlex.split(arg)
        print(args)
        pass

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
