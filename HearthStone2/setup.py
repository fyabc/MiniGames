#! /usr/bin/python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

__author__ = 'fyabc'

# # TODO: Download and install the data here (Using urllib)?
# from urllib.request import urlopen
#
# with open('temp.zip', 'wb') as f, urlopen('https://xxx/temp.zip') as url_f:
#     f.write(url_f.read())

setup(
    name='MyHearthStone',
    version='2.1.0',
    keywords=('HearthStone', 'game'),
    description='A Python implementation of HearthStone.',
    license='MIT',

    url='https://github.com/fyabc/MiniGames/tree/master/HearthStone2',
    author='fyabc',
    author_email='fyabc@mail.ustc.edu.cn',

    packages=find_packages(),
    include_package_data=True,
    platforms='any',
    install_requires=['appdirs>=1.0', 'cocos2d>=0.6', 'pyglet>=1.2.0'],
    extras_require={
        'pyqt-frontend': ['PyQt5>=5.6.0'],
        'kivy-frontend': ['kivy>=1.8.0'],
    },

    scripts=[],
    entry_points={
        'console_scripts': [
            'myhearthstone = MyHearthStone.main:main',
        ]
    },
)
