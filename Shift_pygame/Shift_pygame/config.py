#! /usr/bin/python
# -*- coding: utf-8 -*-

import os

from pygame.colordict import THECOLORS as Colors
import pygame.locals

__author__ = 'fyabc'

# Paths.
PackageRootPath = os.path.dirname(os.path.abspath(__file__))
ResourcePath = os.path.join(PackageRootPath, 'resource')
DataPath = os.path.join(PackageRootPath, 'data')
GameGroupPath = os.path.join(DataPath, 'groups')
RecordPath = os.path.join(DataPath, 'records')
KeymapPath = os.path.join(DataPath, 'keymap.txt')
ImagePath = os.path.join(ResourcePath, 'images')

GameGroupExtension = '.txt'

# Display config.
# [NOTE] X <=> row <=> width, Y <=> column <=> height
WindowWidth = 600
WindowHeight = 600
WindowSize = (WindowWidth, WindowHeight)
ScreenWidth = 600
ScreenHeight = 600
ScreenSize = (ScreenWidth, ScreenHeight)

DefaultCellNumberX = 12
DefaultCellNumberY = 12

assert ScreenHeight % DefaultCellNumberX == 0 and ScreenWidth % DefaultCellNumberY == 0,\
    'The cell number must be a factor of screen size'

DefaultCellWidth = ScreenWidth // DefaultCellNumberX
DefaultCellHeight = ScreenHeight // DefaultCellNumberY

GameTitle = 'Shift-pygame'

# Fonts.
FontSize = 40
FontName = os.path.join(ResourcePath, 'fonts', 'consolas-yahei.ttf')

# FPS.
MainFPS = 60

# Colors.
BackgroundColor = Colors['white']

# Game.
DefaultGroup = 'basic.txt'
GameGroups = os.listdir(GameGroupPath)
