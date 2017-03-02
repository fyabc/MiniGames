#! /usr/bin/python
# -*- encoding: utf-8 -*-

"""Utilities to add arguments to the argument parser."""

__author__ = 'fyabc'


def arg_size(parser, default, help=None):
    parser.add_argument(
        '-s', '--size', metavar='axb', dest='size', default=default, type=str,
        help='The size of the map, format is "axb", default is "{}"'.format(default) if help is None else help
    )
