#! /usr/bin/python
# -*- encoding: utf-8 -*-

"""Change the card data file, so that all cards will have auto increment id."""

import re
import sys

__author__ = 'fyabc'


def main():
    filename = 'HearthStone/data/HearthStoneCard/{}.py'.format(sys.argv[1])
    package_id = 1

    with open(filename, 'r', encoding='utf-8') as f:
        s = f.read()

    i = 1000 * package_id - 1

    def change_id(m):
        nonlocal i

        i += 1
        return '(id={}'.format(i)

    pattern = re.compile(r'\(id=\d+')

    s = pattern.sub(change_id, s)

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(s)


if __name__ == '__main__':
    main()
