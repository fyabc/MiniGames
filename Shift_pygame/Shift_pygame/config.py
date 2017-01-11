#! /usr/bin/python
# -*- coding: utf-8 -*-

import os

__author__ = 'fyabc'

# Paths.
PackageRootPath = os.path.dirname(os.path.abspath(__file__))
ResourcePath = os.path.join(PackageRootPath, 'resource')
DataPath = os.path.join(PackageRootPath, 'data')
GameGroupPath = os.path.join(DataPath, 'groups')
RecordPath = os.path.join(DataPath, 'records')

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

FontSize = 40
FontName = os.path.join(ResourcePath, 'fonts', 'consolas-yahei.ttf')

# Keymap.
KeyMap = {

}

# Game.
DefaultGroup = 'basic.txt'
GameGroups = os.listdir(GameGroupPath)
