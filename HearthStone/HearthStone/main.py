#! /usr/bin/python
# -*- coding: utf-8 -*-

import argparse

__author__ = 'fyabc'


def get_parser():
    parser = argparse.ArgumentParser(description='The Python implementation of HearthStone')

    return parser


def main():
    parser = get_parser()

    print('This is the GUI main script of the package HearthStone!')


if __name__ == '__main__':
    main()
