#! /usr/bin/python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='FyGamePack',
    version='1.0',
    keywords=('mini', 'game', 'pygame'),
    description='A package of some mini games.',
    license='MIT',

    url='https://github.com/fyabc/MiniGames/tree/master/GamePack',
    author='fyabc',
    author_email='fyabc@mail.ustc.edu.cn',

    packages=find_packages(),
    include_package_data=True,
    platforms='any',
    install_requires=['pygame'],

    scripts=[],
    entry_points={
        'console_scripts': [
            'fgp = GamePack.main:main',
            'minesweeper = GamePack.Minesweeper.minesweeper:main',
        ]
    },
)
