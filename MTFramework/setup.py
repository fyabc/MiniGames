# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

__author__ = 'fyabc'

setup(
    name='MTFramework',
    version='0.1',
    keywords=('MTFramework',),
    description='A Python "Magic Tower" game framework.',
    license='MIT',

    url='https://github.com/fyabc/MiniGames/tree/master/MTFramework',
    author='fyabc',
    author_email='fyabc@mail.ustc.edu.cn',

    packages=find_packages(),
    include_package_data=True,
    platforms='any',
    install_requires=[],

    scripts=[],
    entry_points={
        'console_scripts': [
            'mtf = MTFramework.main:main',
        ]
    },
)
