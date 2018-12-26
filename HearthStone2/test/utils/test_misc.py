#! /usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))

import MyHearthStone.utils.misc as misc

__author__ = 'fyabc'


class TestMisc(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    def testTrivialImpl(self):
        class B:
            @misc.trivial_impl
            def f(self):
                pass

        class C(B):
            def f(self):
                pass

        self.assertTrue(misc.is_trivial_impl(B.f))
        self.assertTrue(misc.is_trivial_impl(B().f))
        self.assertFalse(misc.is_trivial_impl(C.f))
        self.assertFalse(misc.is_trivial_impl(C().f))
