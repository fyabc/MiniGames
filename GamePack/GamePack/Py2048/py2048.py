#! /usr/bin/python
# -*- coding: utf-8 -*-

import os
import random
import argparse
import json

import pygame
import pygame.locals

from ..basic.runner import PygameRunner
from ..utils.basic import iter_matrix, parse_size, get_key_name
from ..utils.constant import Colors
from ..utils.arguments import arg_size
from ..utils.path import get_data_path
from .auto_generators import get_auto_iter
from .utils import fill_list

__author__ = 'fyabc'

GameName = 'Py2048'

AllowEvents = (pygame.locals.QUIT, pygame.locals.KEYDOWN,)

Keymap = {
    'exit': [pygame.locals.K_q, ],
    'up': [pygame.locals.K_UP, pygame.locals.K_w, ],
    'down': [pygame.locals.K_DOWN, pygame.locals.K_s, ],
    'left': [pygame.locals.K_LEFT, pygame.locals.K_a, ],
    'right': [pygame.locals.K_RIGHT, pygame.locals.K_d, ],
    'reset': [pygame.locals.K_r, ],
    'auto': [pygame.locals.K_1, pygame.locals.K_2, pygame.locals.K_3, ],
    'manual': [pygame.locals.K_m, ],
}

DefaultRow = 4
DefaultColumn = 4

MinRow = 2
MinColumn = 2

GameData = json.load(open(os.path.join(get_data_path(GameName), 'config.json'), 'r', encoding='utf-8'))

DefaultNameColors = [
    (220, 220, 0, 255),
    (240, 220, 0, 255),
    (220, 190, 190, 255),
    (220, 165, 165, 255),
    (220, 140, 140, 255),
    (220, 115, 115, 255),
    (220, 90, 90, 255),
    (220, 65, 65, 255),
    (220, 40, 40, 255),
    (220, 15, 15, 255),
    (255, 240, 15, 255),
    (255, 255, 30, 255),
    (240, 15, 190, 255),
    (240, 15, 215, 255),
    (240, 15, 240, 255),
    (240, 15, 255, 255),
]

DefaultNames = [
    "2", "4", "8", "16", "32",
    "64", "128", "256", "512", "1024",
    "2048", "4096", "8192", "16384", "32768",
    "65536", "131072", "262144", "524288", "1048576",
    "2097152", "4194304", "8388608", "16777216", "33554432",
    "67108864", "134217728",
]


class GameState:
    # The default probability of 0, the probability of 1 is (1 - Probability_0)
    Probability_0 = 0.9

    Empty = -1

    def __init__(self, row, column, **kwargs):
        self.row = row
        self.column = column
        self.matrix = [[self.Empty for _ in range(column)] for _ in range(row)]
        self.score = 0

        self.prob_0 = kwargs.pop('prob_0', self.Probability_0)
        self.auto_type = kwargs.pop('auto_type', 0)

        self.all_autos = get_auto_iter(self)

        self.reset()

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

    def _get_row(self, row, no_empty=False):
        if no_empty:
            return [v for v in self.matrix[row] if v != self.Empty]
        return self.matrix[row][:]

    def _get_column(self, column, no_empty=False):
        result = [self.matrix[i][column] for i in range(self.row)]

        if no_empty:
            return [v for v in result if v != self.Empty]
        return result

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

        value = 0 if random.random() < self.prob_0 else 1
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

        :return: Boolean if any cells moved.
        """

        moved = False

        for x in range(self.column):
            column_unfiltered = self._get_column(x)

            column = [v for v in column_unfiltered if v != self.Empty]

            new_column = []

            i = len(column) - 1
            while i >= 0:
                if i > 0 and column[i] == column[i - 1]:
                    new_column.append(column[i] + 1)
                    i -= 2
                else:
                    new_column.append(column[i])
                    i -= 1

            new_column.reverse()

            new_column = fill_list(new_column, self.row, self.Empty, left=True)
            for y in range(self.row):
                self[x, y] = new_column[y]

            if not moved and new_column != column_unfiltered:
                moved = True

        return moved

    def down(self):
        moved = False

        for x in range(self.column):
            column_unfiltered = self._get_column(x)

            column = [v for v in column_unfiltered if v != self.Empty]

            new_column = []

            i = 0
            while i < len(column):
                if i < len(column) - 1 and column[i] == column[i + 1]:
                    new_column.append(column[i] + 1)
                    i += 2
                else:
                    new_column.append(column[i])
                    i += 1

            new_column = fill_list(new_column, self.row, self.Empty, left=False)
            for y in range(self.row):
                self[x, y] = new_column[y]

            if not moved and new_column != column_unfiltered:
                moved = True

        return moved

    def left(self):
        moved = False

        for y in range(self.row):
            row_unfiltered = self._get_row(y)

            row = [v for v in row_unfiltered if v != self.Empty]

            new_row = []

            i = len(row) - 1
            while i >= 0:
                if i > 0 and row[i] == row[i - 1]:
                    new_row.append(row[i] + 1)
                    i -= 2
                else:
                    new_row.append(row[i])
                    i -= 1

            new_row.reverse()

            new_row = fill_list(new_row, self.column, self.Empty, left=True)
            for x in range(self.column):
                self[x, y] = new_row[x]

            if not moved and new_row != row_unfiltered:
                moved = True

        return moved

    def right(self):
        moved = False

        for y in range(self.row):
            row_unfiltered = self._get_row(y)

            row = [v for v in row_unfiltered if v != self.Empty]

            new_row = []

            i = 0
            while i < len(row):
                if i < len(row) - 1 and row[i] == row[i + 1]:
                    new_row.append(row[i] + 1)
                    i += 2
                else:
                    new_row.append(row[i])
                    i += 1

            new_row = fill_list(new_row, self.column, self.Empty, left=False)
            for x in range(self.column):
                self[x, y] = new_row[x]

            if not moved and new_row != row_unfiltered:
                moved = True

        return moved


class Py2048(PygameRunner):
    # Some color and style constants.
    BGColor = Colors['white']
    LineColor = Colors['blue']
    TextColor = Colors['black']
    FinalTextColor = Colors['blueviolet']
    
    LineWidth = 4

    FPS = 30
    GenerateDelay = 130
    AutoGenerateDelay = 60

    FontName = 'C:/Windows/Fonts/msyh.ttc'

    NameColors = GameData['NameColors']

    def __init__(self, **kwargs):
        self.row = max(kwargs.pop('row', DefaultRow), MinRow)
        self.column = max(kwargs.pop('column', DefaultColumn), MinColumn)

        self.CellSize = 300 // max(self.row, self.column) + 40

        super().__init__(
            screen_size=(self.CellSize * self.column + 180, self.CellSize * self.row + 180),
            name=GameName,
            allow_events=AllowEvents,
        )

        self.top_left_loc = (self.screen_size[0] // 2 - self.CellSize * self.column // 2,
                             self.screen_size[1] // 2 - self.CellSize * self.row // 2)

        series = kwargs.pop('series', 'common')
        if series not in GameData['AllNames']:
            series = 'common'
        self.AllNames = GameData['AllNames'][series]

        self.state = GameState(self.row, self.column, **kwargs)

    def main_loop(self):
        self.draw()

        running = True
        while running:
            self.timer.tick(self.FPS)

            moved = 0

            if self.state.auto_type == 0:
                for event in pygame.event.get():
                    if event.type == pygame.locals.QUIT:
                        running = False
                    elif event.type == pygame.locals.KEYDOWN:
                        key_name = get_key_name(event.key, Keymap)

                        if key_name == 'exit':
                            running = False
                        elif key_name == 'reset':
                            self.state.reset()
                        elif key_name == 'up':
                            moved = self.state.up()
                        elif key_name == 'down':
                            moved = self.state.down()
                        elif key_name == 'left':
                            moved = self.state.left()
                        elif key_name == 'right':
                            moved = self.state.right()
                        elif key_name == 'auto':
                            self.state.auto_type = event.key - pygame.locals.K_0
            else:
                auto_iter = self.state.all_autos[self.state.auto_type - 1]

                pygame.time.delay(self.AutoGenerateDelay)
                moved = (auto_iter.send(moved))()

                for event in pygame.event.get():
                    if event.type == pygame.locals.QUIT:
                        running = False
                    elif event.type == pygame.locals.KEYDOWN:
                        key_name = get_key_name(event.key, Keymap)

                        if key_name == 'exit':
                            running = False
                        elif key_name == 'reset':
                            self.state.reset()
                        elif key_name == 'auto':
                            self.state.auto_type = event.key - pygame.locals.K_0
                        elif key_name == 'manual':
                            self.state.auto_type = 0

            self.draw()

            if moved > 0:
                pygame.time.delay(self.GenerateDelay if self.state.auto_type == 0 else self.AutoGenerateDelay)
                self.state.generate()
                self.draw()

            if self.state.lose():
                text = self.get_font(self.FontName, 70).render('You Lose!', True, self.FinalTextColor, None)
                text_rect = text.get_rect()
                text_rect.center = self.screen_size[0] / 2, self.screen_size[1] / 2

                self.main_window.blit(text, text_rect)
                pygame.display.update()

                pygame.time.delay(1500)

                self.state.reset()

    def draw(self):
        self.draw_background()

        score_font = self.get_font(self.FontName, 50)
        score_text = score_font.render('Score: {}'.format(self.state.score), True, self.TextColor)
        score_rect = score_text.get_rect()
        score_rect.center = self.screen_size[0] * 0.5, self.screen_size[1] * 0.05

        self.main_window.blit(score_text, score_rect)

        font = self.get_font(self.FontName, self.CellSize // 2)

        for x, y in iter_matrix(self.row, self.column):
            value = self.state[x, y]

            font = self.get_font(self.FontName, self._get_font_size(value))

            if value != self.state.Empty:
                cell_rect = pygame.Rect(0, 0, int(self.CellSize * 0.8), int(self.CellSize * 0.8))
                cell_rect.center = (self.top_left_loc[0] + (x + 0.5) * self.CellSize,
                                    self.top_left_loc[1] + (y + 0.5) * self.CellSize)
                pygame.draw.rect(self.main_window, self.NameColors[value], cell_rect, 0)

                text = font.render(self.AllNames[value], True, Colors['white'], None)
                text_rect = text.get_rect()
                text_rect.center = cell_rect.center
                self.main_window.blit(text, text_rect)

        pygame.display.update()

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

    def _get_font_size(self, value):
        size = len(self.AllNames[value])

        if size <= 2:
            return self.CellSize // 2
        else:
            return int(self.CellSize * 1.4 // size)


def real_main(options):
    row, column = parse_size(options.size)

    game = Py2048(row=row, column=column, prob_0=options.prob_0, series=options.series)

    game.run()


def build_parser():
    parser = argparse.ArgumentParser(prog='py2048', description='A simple implementation of 2048.')

    arg_size(parser, default='4x4', help='The size of the map, format is "axb", default is "4x4" '
                                         '(a must >= {}, b must >= {}).'.format(MinRow, MinColumn))
    parser.add_argument('-p', '--prob', metavar='P', dest='prob_0', default=GameState.Probability_0, type=float,
                        help='The probability of generate the level 0 cell, default is {}.'.format(GameState.Probability_0))
    parser.add_argument('-S', '--series', metavar='name', dest='series', action='store', default='common', type=str,
                        help='The name series, default is common.')

    return parser


def main():
    parser = build_parser()

    options = parser.parse_args()

    real_main(options)
