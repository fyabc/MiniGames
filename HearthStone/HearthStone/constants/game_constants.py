#! /usr/bin/python
# -*- coding: utf-8 -*-

"""Constants of the game."""

__author__ = 'fyabc'

TotalPlayerNumber = 2
MaxDeckNumber = 50
MaxHandNumber = 10
MaxDeskNumber = 7
MaxCrystal = 10

# Insert the new minion to the left or the right of the desk.
DeskLocationLeft = 0
DeskLocationRight = max(MaxDeckNumber, MaxDeskNumber, MaxHandNumber) + 10
