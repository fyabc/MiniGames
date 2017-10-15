#! /usr/bin/python
# -*- coding: utf-8 -*-

import argparse

__author__ = 'fyabc'


def main():
    # Parse arguments.
    parser = argparse.ArgumentParser(description='My HearthStone Game.')
    args = parser.parse_args()

    # Load project config.
    # [NOTE]: This must before the import of any other game modules.
    from .utils.constants import load_arg_config
    load_arg_config(args)

    from .game.core import Game
    game = Game()

    # todo


if __name__ == '__main__':
    main()
