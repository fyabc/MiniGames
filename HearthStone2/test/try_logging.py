#! /usr/bin/python
# -*- coding: utf-8 -*-

import logging

__author__ = 'fyabc'


def main():
    logging.basicConfig(
        level='INFO',
        style='{',
        format='[{levelname:<8}] {asctime}.{msecs:0>3.0f}: <{pathname}:{lineno}> {message}',
        datefmt='%Y-%m-%d %H:%M:%S',
    )
    logging.addLevelName(25, 'COMMON')
    logging.debug('Hello world debug!')
    logging.info('Hello world info!')
    logging.warning('Hello world warning!')
    logging.error('Hello world error!')
    logging.critical('Hello world critical!')
    logging.log(25, 'Hello world common!')


if __name__ == '__main__':
    main()
