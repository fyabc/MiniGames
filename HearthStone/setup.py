# -*- coding: utf-8 -*-

__author__ = 'fyabc'

from setuptools import setup, find_packages

setup(
    name='HearthStone',
    version='1.0',
    keywords=('HearthStone',),
    description='A Python implementation of HearthStone.',
    license='MIT',

    url='https://github.com/fyabc/MiniGames/tree/master/HearthStone',
    author='fyabc',
    author_email='fyabc@mail.ustc.edu.cn',

    packages=find_packages(),
    include_package_data=True,
    platforms='any',
    install_requires=[],

    scripts=[],
    entry_points={
        'console_scripts': [
            'hearthstone = HearthStone.main:main',
        ]
    },
)
