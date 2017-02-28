#! /usr/bin/python
# -*- encoding: utf-8 -*-

import argparse

import pygame
import pygame.locals

from ..basic.runner import PygameRunner
from ..utils.basic import parse_size, get_key_name, load_image
from ..utils.constant import Colors, FPS
from ..utils.path import get_data_path

__author__ = 'fyabc'


GameName = 'Minesweeper'

AllowEvents = (pygame.locals.QUIT, pygame.locals.MOUSEBUTTONDOWN, pygame.locals.KEYDOWN,)

DefaultRow = 15
DefaultColumn = 30
DefaultMineNumber = 99

MinRow = 5
MinColumn = 5
MinMineNumber = 4
MinRemainSpaceNumber = 8


Keymap = {
    'exit': [pygame.locals.K_q, ],
    'restart': [pygame.locals.K_r, ],
    'sweep': [pygame.locals.K_s, ],
    'flag': [pygame.locals.K_f, ],
    'quick': [pygame.locals.K_k, ],
}

Direction8 = (
    (1, 0), (-1, 0), (0, 1), (0, -1),
    (1, 1), (1, -1), (-1, 1), (-1, -1)
)


class GameState:
    def __init__(self, row, column, mine_num, todo_tag=False):
        pass


class Minesweeper(PygameRunner):
    # Some color and style constants.
    BGColor = Colors['gray10']
    LineColor = Colors['black']
    SweptColor = Colors['whitesmoke']
    UnsweptColor = Colors['gray30']
    TextColor = Colors['black']

    NumberColors = (
        Colors['black'],  # This is index 0, represents mine.
        Colors['blue'],
        Colors['green'],
        Colors['red'],
        Colors['brown4'],
        Colors['lightblue4'],
        Colors['black'],
        Colors['gray'],
        Colors['gray100'],
    )

    LineWidth = 1

    def __init__(self, **kwargs):
        self.row = max(kwargs.pop('row', DefaultRow), MinRow)
        self.column = max(kwargs.pop('column', DefaultColumn), MinColumn)

        super().__init__(
            screen_size=(self.column * 45, self.row * 45),
            name=GameName,
            allow_events=AllowEvents,
        )

        self.cell_size = int(min(self.screen_size[0] / self.column, self.screen_size[1] / self.row) * 0.8)
        self.top_left_loc = (self.screen_size[0] // 2 - self.cell_size * self.column // 2,
                             int(self.screen_size[1] * 0.55) - self.cell_size * self.row // 2)

        self.mine_number = kwargs.pop('mine_number', DefaultMineNumber)
        self.mine_number = min(self.mine_number, self.row * self.column - MinRemainSpaceNumber)
        self.mine_number = max(self.mine_number, MinMineNumber)

        self.state = GameState(self.row, self.column, self.mine_number, todo_tag=kwargs.pop('todo_tag', False))
    
    def main_loop(self):
        running = True

        self.draw()

        while running:
            events = pygame.event.get()

            for event in events:
                if event.type == pygame.locals.QUIT:
                    running = False

            if events:
                self.draw()

    def draw(self):
        self.draw_background()

        pygame.display.update()

    def draw_background(self):
        self.main_window.fill(self.BGColor)

        for x in range(self.column + 1):
            pygame.draw.line(
                self.main_window, self.LineColor,
                (self.top_left_loc[0] + x * self.cell_size, self.top_left_loc[1]),
                (self.top_left_loc[0] + x * self.cell_size, self.top_left_loc[1] + self.row * self.cell_size),
                self.LineWidth,
            )

        for y in range(self.row + 1):
            pygame.draw.line(
                self.main_window, self.LineColor,
                (self.top_left_loc[0], self.top_left_loc[1] + y * self.cell_size),
                (self.top_left_loc[0] + self.column * self.cell_size, self.top_left_loc[1] + y * self.cell_size),
                self.LineWidth,
            )


def real_main(options):
    row, column = parse_size(options.size)

    game = Minesweeper(row=row, column=column, mine_number=options.mine_number, todo_tag=options.todo_tag)

    game.run()


def build_parser():
    parser = argparse.ArgumentParser(description='A simple implementation of minesweeper game.')
    parser.add_argument('-s', '--size', metavar='axb', dest='size', default='15x30', type=str,
                        help='The size of the map, format is "axb", default is "15x30" '
                             '(a must >= {}, b must >= {}).'.format(MinRow, MinColumn))
    parser.add_argument('-n', '--number', metavar='N', dest='mine_number', default=99, type=int,
                        help='The number of mines, default is 99 '
                             '(N must >= {}, must <= a * b - {}).'.format(MinMineNumber, MinRemainSpaceNumber))
    parser.add_argument('-t', '--todo', action='store_true', dest='todo_tag', default=False,
                        help='Add todo tag, default is False.')

    return parser


def main():
    parser = build_parser()

    options = parser.parse_args()

    real_main(options)
