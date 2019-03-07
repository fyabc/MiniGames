#! /usr/bin/python
# -*- coding: utf-8 -*-

import unittest

from MyHearthStone.utils.config_class import *

__author__ = 'fyabc'


class ConfigTest(unittest.TestCase):
    d = {
        "ProjectName": "HearthStone",
        "Locale": None,
        "DefaultLocale": "zh_CN",
        "Frontend": "text-single",
        "EnableUserExtension": True,
        "UserExtensionPaths": [],
        "Logging": {
            "Level": "INFO",
            "ScreenLog": False,
            "Width": 80
        },
        "Game": {
            "Version": [9, 1, 0],

            "DeckSize": 30,
            "SameCardMax": [2, 2, 2, 2, 1],

            "DeckMax": 60,
            "HandMax": 10,
            "PlayMax": 7,
            "SecretMax": 5,
            "ManaMax": 10,

            "TurnMax": 89,

            "StartCardOffensive": 3,
            "StartCardDefensive": 4
        },
        "UI": {
            "Cocos": {
                "WindowSize": [1280, 700]
            }
        }
    }

    def setUp(self):
        self.c = Configuration.from_dict(self.d)

    def testBasic(self):
        self.assertEqual(self.c.UI.Cocos.WindowSize, [1280, 700])

        self.c.UI.Cocos.WindowSize = 10
        self.assertEqual(self.c.UI.Cocos.WindowSize, 10)

    def testRepr(self):
        c_str = repr(self.c)

        self.assertEqual(len(c_str), 558)
        self.assertEqual(c_str.count('Configuration'), 5)
        self.assertIn('[1280, 700]', c_str)
        self.assertIn("'ScreenLog': False", c_str)

    def testUpdate(self):
        arg_config = Configuration.from_dict({
            'Frontend': 'cocos-single',
            'Logging': {
                'Level': 'DEBUG',
                'ScreenLog': True,
            }
        })

        self.c.update(arg_config)

        self.assertEqual(self.c.Logging.ScreenLog, True)
        self.assertEqual(self.c.Frontend, 'cocos-single')
        self.assertEqual(self.c.Logging.Level, 'DEBUG')

        # NOTE: `update` method will replace the sub-dict, so the attribute `Logging.Width` will disappear.
        with self.assertRaises(AttributeError):
            print(self.c.Logging.Width)

    def testIterUpdate(self):
        arg_config = Configuration.from_dict({
            'Frontend': 'cocos-single',
            'Logging': {
                'Level': 'DEBUG',
                'ScreenLog': True,
            }
        })

        self.c.iter_update(arg_config)

        self.assertEqual(self.c.Logging.ScreenLog, True)
        self.assertEqual(self.c.Frontend, 'cocos-single')
        self.assertEqual(self.c.Logging.Level, 'DEBUG')
        self.assertEqual(self.c.Logging.Width, 80)  # Note here

    def testPickle(self):
        import pickle

        pickled = pickle.dumps(self.c)
        new_c = pickle.loads(pickled)

        self.assertEqual(self.c, new_c)
