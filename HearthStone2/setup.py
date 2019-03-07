#! /usr/bin/python
# -*- coding: utf-8 -*-

import os
from setuptools import setup, find_packages

__author__ = 'fyabc'

# # TODO: Download and install the data here (Using urllib)?
# from urllib.request import urlopen
#
# with open('temp.zip', 'wb') as f, urlopen('https://xxx/temp.zip') as url_f:
#     f.write(url_f.read())


def _read_metadata():
    """Read project metadata from *__metadata__.py*."""
    metadata_filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'MyHearthStone', '__metadata__.py')
    metadata = {}
    with open(metadata_filename, 'r', encoding='utf-8') as f:
        exec(f.read(), metadata)
    return metadata


_metadata = _read_metadata()

setup(
    name=_metadata['__title__'],
    version=_metadata['__version__'],
    keywords=_metadata['__keywords__'],
    description=_metadata['__description__'],
    license=_metadata['__license__'],

    url=_metadata['__url__'],
    author=_metadata['__author__'],
    author_email=_metadata['__author_email__'],

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
