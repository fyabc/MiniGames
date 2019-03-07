#! /usr/bin/python
# -*- coding: utf-8 -*-

import unittest

from MyHearthStone.utils import constants

__author__ = 'fyabc'


class TestConstants(unittest.TestCase):
    def setUp(self):
        self.orig_C = constants.C.copy()

    def tearDown(self):
        constants.C = self.orig_C

    def testLoadArgConfig(self):
        constants.load_arg_config({
            'Frontend': 'text-single',
            'Logging': {
                'Level': 'WARNING',
                'ScreenLog': False,
            }
        })

        self.assertEqual(constants.C.Frontend, 'text-single')
        self.assertEqual(constants.C.Logging.Level, 'WARNING')
        self.assertEqual(constants.C.Game.Version, self.orig_C.Game.Version)

    def testGetPackagePaths(self):
        package_paths = constants.get_package_paths()
        self.assertIn(constants.SystemPackageDataPath, package_paths)
