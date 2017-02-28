#! /usr/bin/python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

__author__ = 'fyabc'

setup(
    name='Shift_cocos2d',
    version='1.0',
    keywords=('Shift', 'cocos2d'),
    description='A Python implementation of Shift, using cocos2d library.',
    license='MIT',

    url='https://github.com/fyabc/MiniGames/tree/master/Shift_cocos2d',
    author='fyabc',
    author_email='fyabc@mail.ustc.edu.cn',

    packages=find_packages(),
    include_package_data=True,
    platforms='any',
    install_requires=['cocos2d'],

    scripts=[],
    entry_points={
        'console_scripts': [
            'shift-cocos2d = Shift_cocos2d.main:main',
        ],
    },
)
