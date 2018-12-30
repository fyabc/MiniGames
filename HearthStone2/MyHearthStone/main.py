#! /usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import sys

__author__ = 'fyabc'


def main():
    # Parse arguments.
    parser = argparse.ArgumentParser(description='My HearthStone Game.')

    group_basic = parser.add_argument_group('Basic', 'basic settings')
    group_basic.add_argument('-l', '--log-level', metavar='level', action='store', default='info',
                             dest='debug_level', choices=['debug', 'verbose', 'info', 'warning', 'error', 'critical'],
                             help='Game logging level, default is "%(default)r"')
    group_basic.add_argument('-L', '--scr-log', action='store_true', default=False, dest='screen_log',
                             help='Show logging message into screen, default is %(default)r')
    group_basic.add_argument('-f', '--frontend', metavar='mode', action='store', default='cocos-single',
                             dest='frontend', help='Choose game frontend, default is "%(default)r"')
    group_basic.add_argument('-u', '--user', metavar='name', action='store', default=None, dest='user_id_or_name',
                             help='User name, default is %(default)r, will override value of "--uid"')
    group_basic.add_argument('--uid', metavar='ID', action='store', default=None, type=int, dest='user_id_or_name',
                             help='User id, default is %(default)r, will override value of "-u"')

    group_locale = parser.add_argument_group('Locale', 'locale settings')
    group_locale.add_argument('--locale', metavar='LOCALE', default=None, type=str, dest='locale',
                              help='Locale string, default is None (use system default locale)')
    
    group_debug = parser.add_argument_group('Debug', 'debug settings')
    group_debug.add_argument('--raise', action='store_true', default=False, dest='raise_exception',
                             help='Re-raise exceptions in the game, not stop them, default is %(default)r')
    
    # TODO: add more arg options

    args = parser.parse_args()

    # print(args)
    # exit()

    # Load project config.
    # [NOTE]: This must before the import of any other game modules.
    from .utils.constants import load_arg_config
    arg_config = {
        'Frontend': args.frontend,
        'Logging': {
            'Level': args.debug_level.upper(),
            'ScreenLog': args.screen_log,
        },
    }
    if args.locale is not None:
        arg_config['Locale'] = args.locale
    load_arg_config(arg_config)

    # [NOTE]: The import of C must after the loading of arg config.
    from .utils.constants import C
    from .utils.message import setup_logging
    from .utils import monkey_patch
    from .ui import get_frontend

    setup_logging(level=C.Logging.Level, scr_log=C.Logging.ScreenLog)

    frontend = get_frontend(C.Frontend)(
        user_id_or_name=args.user_id_or_name,
        raise_exception=args.raise_exception,
    )
    sys.exit(frontend.main())


if __name__ == '__main__':
    main()
