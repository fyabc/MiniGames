#! /usr/bin/python
# -*- coding: utf-8 -*-

from .utils.package_io import all_cards

__author__ = 'fyabc'


def main():
    AllCards = all_cards()

    print(AllCards)


if __name__ == '__main__':
    main()
