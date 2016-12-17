#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'fyabc'

# [NOTE] Move some processes into handler to avoid circle reference.
# Example: Add a coin to the opponent's hand.
#     Add this to event `GameEnd` may cause circle reference.
