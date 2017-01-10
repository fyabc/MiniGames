#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'fyabc'

from setuptools import setup, find_packages

setup(
    name='Shift_cocos2d',
    version='1.0',
    keywords=('Shift',),
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
