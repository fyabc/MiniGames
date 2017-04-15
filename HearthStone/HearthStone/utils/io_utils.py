#! /usr/bin/python
# -*- encoding: utf-8 -*-

import os

from .config import AppDataPath

__author__ = 'fyabc'


def make_directories():
    """Make some needed user data directory and log directory."""

    try:
        os.makedirs(AppDataPath.user_data_dir, exist_ok=True)
        os.makedirs(AppDataPath.user_log_dir, exist_ok=True)
    except:
        print('ERROR: Cannot create directories.')


def load_decks():
    """Load deck from user data directory.
    
    :return: List of dict, each dict is a deck.
    """

    decks = []

    return decks


def save_decks(decks):
    """Save decks to data directory.
    
    :param decks: List of dict, each dict is a deck.
    """


__all__ = [
    'make_directories',
    'load_decks',
    'save_decks',
]
