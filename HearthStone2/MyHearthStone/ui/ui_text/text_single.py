#! /usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import cmd
import shlex

from ...game.core import Game
from ...game.deck import Deck
from ...game import player_action as pa
from ..frontend import Frontend
from ...utils.constants import C
from ...utils.game import Klass, Zone
from ...utils.message import error, info
from ...utils.package_io import search_by_name, all_cards
from ...utils.cocos_draw import draw_game, draw_game_spawn

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

    def __init__(self, frontend: 'TextSingleFrontend'):
        super().__init__()
        self.frontend = frontend
        self.state = self.StateMain
        self.prompt = 'HS[main]> '  # Init prompt

        # Command parsers.
        self.parser_user = NoExitParser(prog='user')
        self.sub_user = self.parser_user.add_subparsers(dest='action')
        self.sub_user.default = 'show'
        parser_user_show = self.sub_user.add_parser('show')
        parser_user_all = self.sub_user.add_parser('all')
        parser_user_name = self.sub_user.add_parser('name')
        parser_user_name.add_argument('new_name', nargs='?', default=None, help='New name, default is None')

        self.parser_deck = NoExitParser(prog='deck')
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
        delete_group.add_argument('-n', '--name', action='store', dest='name', default=None,
                                  help='Delete by name, default is None')
        parser_deck_show = self.sub_deck.add_parser('show')

        self.parser_game = NoExitParser(prog='game')
        self.parser_game.add_argument('-m', '--mode', action='store', dest='mode', default='standard',
                                      help='Game mode, default is %(default)s.')
        deck1_group = self.parser_game.add_mutually_exclusive_group(required=True)
        deck1_group.add_argument('-1', '--deck1', action='store', dest='deck1', metavar='name', default=None,
                                 help='Name of deck 1.')
        deck1_group.add_argument('-x', '--id1', action='store', dest='deck1_id', metavar='N', type=int, default=None,
                                 help='Index of deck 1.')
        deck2_group = self.parser_game.add_mutually_exclusive_group(required=True)
        deck2_group.add_argument('-2', '--deck2', action='store', dest='deck2', metavar='name', default=None,
                                 help='Name of deck 2.')
        deck2_group.add_argument('-y', '--id2', action='store', dest='deck2_id', metavar='N', type=int, default=None,
                                 help='Index of deck 2.')

        self.parser_draw = NoExitParser(prog='draw')
        self.parser_draw.add_argument('-S', '--no-spawn', action='store_false', dest='spawn', default=True,
                                      help='Do not spawn a new process, default will spawn.')

    def emptyline(self):
        """Do nothing when enter an empty line."""
        pass

    def postcmd(self, stop, line):
        """Update prompt after each command."""
        if self.state == self.StateGame:
            assert self.frontend.game is not None
            player_str = '(P{})'.format(self.frontend.game.current_player)
        else:
            player_str = ''
        self.prompt = self.prompt_pattern.format(self.state, player_str)
        return stop

    def do_quit(self, arg):
        """\
Terminate the application.
Syntax: q | quit | exit\
"""
        if self.state == self.StateGame:
            while True:
                confirm = input('The game is running. Are you sure to concede? (y/n) ').lower()
                if confirm == 'y':
                    game = self.frontend.game
                    game.run_player_action(pa.Concede(game))
                    return True
                elif confirm == 'n':
                    info('Nothing happens.')
                    return
                else:
                    pass
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

    def help_user(self):
        self.parser_user.print_help()

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
            # Set deck name and class.
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

            # Add cards.
            print('Add cards: (<card name / id> [<card number>]), type q to quit')
            card_id_list = []
            while True:
                words = input('> ').strip().split()

                if not words:
                    continue
                if words[0] == 'q':
                    break

                words = words[:2]
                if len(words) == 1:
                    n_cards = 1
                else:
                    try:
                        n_cards = int(words[1])
                    except ValueError:
                        print('The second argument must be a number.')
                        continue

                try:
                    card_id = int(words[0])
                    if card_id not in all_cards():
                        card_id = None
                except ValueError:
                    card_id = search_by_name(words[0])

                if card_id is None:
                    print('Cannot found the card.')
                    continue

                card_id_list.extend(card_id for _ in range(n_cards))
            card_id_list = sorted(card_id_list)

            decks.append(Deck(klass=klass, card_id_list=card_id_list, name=name))
            info('Create new deck: {}[{}]'.format(name, klass_name))
        elif args.action == 'delete':
            if args.name is not None:
                try:
                    index = ([d.name for d in decks]).index(args.name)
                except ValueError:
                    error('Cannot find deck {!r}.'.format(args.name))
                    return
            else:
                if not 0 <= args.index < len(decks):
                    error('Index out of range.')
                    return
                index = args.index
            while True:
                confirm = input('> Delete deck {} {}, confirm? (y/n) '.format(index, decks[index])).lower()
                if confirm == 'y':
                    info('Deck {} {} deleted.'.format(index, decks[index]))
                    del decks[index]
                    return
                elif confirm == 'n':
                    info('Nothing happens.')
                    return
                else:
                    pass

    def help_deck(self):
        self.parser_deck.print_help()

    def complete_deck(self, *args):
        return [c for c in self.sub_deck.choices if c.startswith(args[0])]

    #################
    # Game commands #
    #################

    def do_game(self, arg):
        try:
            args = self.parser_game.parse_args(shlex.split(arg))
        except ParserExit:
            return

        if not self._check_state(self.StateMain):
            return

        decks = self.frontend.user.decks

        # Load decks.
        def _get_deck(deck_name, deck_id, n=1):
            if deck_name is None:
                try:
                    return decks[deck_id]
                except IndexError:
                    print('Deck {} index not in range'.format(n))
                    return None
            else:
                for deck in decks:
                    if deck.name == deck_name:
                        return deck
                return None

        deck1 = _get_deck(args.deck1, args.deck1_id, 1)
        if deck1 is None:
            return
        deck2 = _get_deck(args.deck2, args.deck2_id, 2)
        if deck2 is None:
            return

        # Start game processing.
        game = self.frontend.game = Game(frontend=self.frontend, error_stub=self.frontend.game_error)
        start_game_iter = game.start_game([deck1, deck2], mode=args.mode)
        try:
            next(start_game_iter)

            def _get_replace(p=0):
                prompt = 'P{}: {}\nSelect card to replace: '.format(p, game.format_zone(Zone.Hand, p))
                hand_len = len(game.get_zone(Zone.Hand, p))
                while True:
                    r_s = input(prompt).strip().split()
                    try:
                        r = [int(e) for e in r_s]
                        for i in r:
                            if not -hand_len <= i < hand_len:
                                print('Index {} out of range.'.format(i))
                                break
                        else:
                            return r
                    except ValueError:
                        print('Please input list of indices.')

            r0 = _get_replace(0)
            r1 = _get_replace(1)

            start_game_iter.send([r0, r1])
        except StopIteration:
            pass

        # Now in game main loop.
        self.state = self.StateGame

    def do_info(self, arg):
        import textwrap
        for card in all_cards().values():
            print('{}{}:'.format(card.data['name'], card.data['CAH']))
            print(textwrap.indent(card.data['description'], '    '))
            print()

    def help_game(self):
        self.parser_game.print_help()

    def do_draw(self, arg):
        try:
            args = self.parser_draw.parse_args(shlex.split(arg))
        except ParserExit:
            return

        if args.spawn:
            draw_game_spawn(self.frontend.game)
        else:
            draw_game(self.frontend.game)

    def help_draw(self):
        self.parser_draw.print_help()

    # Player actions.
    def do_turnend(self, arg):
        if not self._check_state(self.StateGame):
            return

        game = self.frontend.game
        game.run_player_action(pa.TurnEnd(game))

        self._update_state()

    do_te = do_turnend

    def do_concede(self, arg):
        if not self._check_state(self.StateGame):
            return

        game = self.frontend.game
        game.run_player_action(pa.Concede(game))

        self._update_state()

    def do_play(self, arg):
        if not self._check_state(self.StateGame):
            return

        # todo
        # self.game.run_player_action(pa.PlayMinion(self.game, ))

    def _check_state(self, state):
        result = state == self.state
        if not result:
            print('This command must run in mode {!r}.'.format(state))
        return result

    def _update_state(self):
        if self.state == self.StateGame:
            if self.frontend.game is None or not self.frontend.game.running:
                self.state = self.StateMain


class TextSingleFrontend(Frontend):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.session = TextSingleSession(self)

    @staticmethod
    def game_error(*args, **kwargs):
        print('Game error: ', end='')
        print(*args, **kwargs)

    def _main(self):
        self.session.cmdloop()


__all__ = [
    'TextSingleFrontend',
]
