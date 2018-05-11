#! /usr/bin/python
# -*- coding: utf-8 -*-

"""A simple in-memory card database. Used by random cards."""

__author__ = 'fyabc'


def _default_prob_fn(card):
    """The default probability function, returns same probability for all cards."""
    return 1.0


def _discover_prob_fn(card):
    """The probability function commonly used in 'discover'. Class cards have 3x probability."""


def random_card(condition, prob_fn=_default_prob_fn):
    """

    :param condition:
    :param prob_fn:
    :return:
    """
    pass
