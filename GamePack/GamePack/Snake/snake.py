#! /usr/bin/python
# -*- encoding: utf-8 -*-

import argparse

from ..basic.runner import PygameRunner

__author__ = 'fyabc'


class Snake(PygameRunner):
    def main_loop(self):
        pass


def real_main(options):
    pass


def build_parser():
    parser = argparse.ArgumentParser(description='A simple implementation of Snake.')

    return parser


def main():
    parser = build_parser()

    options = parser.parse_args()

    real_main(options)
