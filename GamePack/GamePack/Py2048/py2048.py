#! /usr/bin/python
# -*- coding: utf-8 -*-

import random
import argparse

import pygame
import pygame.locals

from ..basic.runner import PygameRunner
from ..utils.basic import iter_matrix
from ..utils.constant import Colors

__author__ = 'fyabc'

GameName = 'Py2048'

AllowEvents = (pygame.locals.QUIT, pygame.locals.KEYDOWN,)

DefaultRow = 4
DefaultColumn = 4

MinRow = 2
MinColumn = 2


class GameState:
    # The probability of 0, the probability of 1 is (1 - Probability_0)
    Probability_0 = 0.1

    Empty = -1

    def __init__(self, row, column, **kwargs):
        self.row = row
        self.column = column
        self.matrix = [[self.Empty for _ in range(column)] for _ in range(row)]
        self.score = 0

    def split_loc(self, *location):
        if len(location) >= 2:
            return location[0], location[1]
        else:
            location = location[0]
            if hasattr(location, '__len__'):
                return location
            else:
                return location % self.column, location // self.column

    def __getitem__(self, item):
        x, y = self.split_loc(item)
        return self.matrix[y][x]

    def __setitem__(self, key, value):
        x, y = self.split_loc(key)
        self.matrix[y][x] = value

    def empty(self, x, y):
        return self[x, y] == self.Empty

    def rand_loc(self):
        locations = [(x, y) for x in range(self.column) for y in range(self.row) if self.empty(x, y)]

        if not locations:
            return None

        return random.choice(locations)

    def generate(self):
        loc = self.rand_loc()
        if loc is None:
            return False

        value = 0 if random.random() < self.Probability_0 else 1
        self[loc] = value

        return True

    def reset(self):
        self.score = 0

        for x, y in iter_matrix(self.row, self.column):
            self[x, y] = self.Empty

        self.generate()
        self.generate()

    def lose(self):
        for x, y in iter_matrix(self.row, self.column):
            # Have empty cell
            if self[x, y] == self.Empty:
                return False
            # Have cell that can be merged
            if x < self.column - 1 and self[x, y] == self[x + 1, y]:
                return False
            if y < self.row - 1 and self[x, y] == self[x, y + 1]:
                return False
        return True

    def up(self):
        """Execute the command 'up'.

        :return: Number of moved cells.
        """
        moved = 0

        for x, y in iter_matrix(self.row, self.column):
            value = self[x, y]

            if value == self.Empty:
                continue

            new_y = y
            while new_y > 0 and self.empty(x, new_y - 1):
                new_y -= 1

            self[x, y] = self.Empty

            if new_y > 0 and self[x, new_y - 1] == value:
                # merge
                self[x, new_y - 1] = value + 1
                self.score += (4 << value)
                new_y -= 1
            else:
                # not merge
                self[x, new_y] = value

            if new_y != y:
                moved += 1

        return moved

    def down(self):
        moved = 0

        for x, y in iter_matrix(self.row, self.column):
            value = self[x, y]

            if value == self.Empty:
                continue

            new_y = y
            while new_y < self.row - 1 and self.empty(x, new_y + 1):
                new_y += 1

            self[x, y] = self.Empty

            if new_y < self.row - 1 and self[x, new_y + 1] == value:
                # merge
                self[x, new_y + 1] = value + 1
                self.score += (4 << value)
                new_y += 1
            else:
                # not merge
                self[x, new_y] = value

            if new_y != y:
                moved += 1

        return moved

    def left(self):
        moved = 0

        for x, y in iter_matrix(self.row, self.column):
            value = self[x, y]

            if value == self.Empty:
                continue

            new_x = x
            while new_x > 0 and self.empty(new_x - 1, y):
                new_x -= 1

            self[x, y] = self.Empty

            if new_x > 0 and self[new_x - 1, y] == value:
                # merge
                self[new_x - 1, y] = value + 1
                self.score += (4 << value)
                new_x -= 1
            else:
                # not merge
                self[new_x, y] = value

            if new_x != x:
                moved += 1

        return moved

    def right(self):
        moved = 0

        for x, y in iter_matrix(self.row, self.column):
            value = self[x, y]

            if value == self.Empty:
                continue

            new_x = x
            while new_x < self.column - 1 and self.empty(new_x + 1, y):
                new_x += 1

            self[x, y] = self.Empty

            if new_x < self.column - 1 and self[new_x + 1, y] == value:
                # merge
                self[new_x - 1, y] = value + 1
                self.score += (4 << value)
                new_x += 1
            else:
                # not merge
                self[new_x, y] = value

            if new_x != x:
                moved += 1

        return moved


class Py2048(PygameRunner):
    # Some color and style constants.
    BGColor = Colors['white']
    LineColor = Colors['blue']
    TextColor = Colors['black']
    
    LineWidth = 4
    
    CellSize = 100

    def __init__(self, **kwargs):
        self.row = max(kwargs.pop('row', DefaultRow), MinRow)
        self.column = max(kwargs.pop('column', DefaultColumn), MinColumn)

        super().__init__(
            screen_size=(self.column * self.CellSize + 140, self.row * self.CellSize + 140),
            name=GameName,
            allow_events=AllowEvents,
        )

        self.top_left_loc = (self.screen_size[0] // 2 - self.CellSize * self.column // 2,
                             self.screen_size[1] // 2 - self.CellSize * self.row // 2)

    def main_loop(self):
        pass

    def draw(self):
        pass

    def draw_background(self):
        self.main_window.fill(self.BGColor)

        for x in range(self.column + 1):
            pygame.draw.line(
                self.main_window, self.LineColor,
                (self.top_left_loc[0] + x * self.CellSize, self.top_left_loc[1]),
                (self.top_left_loc[0] + x * self.CellSize, self.top_left_loc[1] + self.row * self.CellSize),
                self.LineWidth,
            )

        for y in range(self.row + 1):
            pygame.draw.line(
                self.main_window, self.LineColor,
                (self.top_left_loc[0], self.top_left_loc[1] + y * self.CellSize),
                (self.top_left_loc[0] + self.column * self.CellSize, self.top_left_loc[1] + y * self.CellSize),
                self.LineWidth,
            )


def real_main(options):
    pass


def build_parser():
    parser = argparse.ArgumentParser(prog='py2048', description='A simple implementation of 2048.')

    return parser


def main():
    parser = build_parser()

    options = parser.parse_args()

    real_main(options)
