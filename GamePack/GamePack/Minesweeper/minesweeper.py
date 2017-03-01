#! /usr/bin/python
# -*- encoding: utf-8 -*-

import random
from collections import deque
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
    Lose = -1
    Win = 1
    Common = 0

    class Cell:
        Nothing = 0
        Flag = 1
        Todo = 2

        def __init__(self, owner):
            self.owner = owner
            self.have_mine = False
            self.adj_mine_num = 0
            self.swept = False
            self.tag = self.Nothing

        def sweep(self):
            if self.swept:
                return False

            self.owner.swept_num += 1
            self.swept = True
            self.tag = self.Nothing

            if self.tag == self.Flag:
                self.owner.flagged_mine_num -= 1
            return self.have_mine

        def change_tag(self, newTag):
            if self.tag == self.Flag:
                self.owner.flagged_mine_num -= 1
            self.tag = newTag
            if self.tag == self.Flag:
                self.owner.flagged_mine_num += 1

        def next_tag(self):
            if self.tag == self.Flag:
                self.owner.flagged_mine_num -= 1
            self.tag = (self.tag + 1) % (3 if self.owner.todo_tag else 2)
            if self.tag == self.Flag:
                self.owner.flagged_mine_num += 1

    def split_loc(self, *location):
        if len(location) >= 2:
            return location[0], location[1]
        else:
            location = location[0]
            if hasattr(location, '__len__'):
                return location
            else:
                return location % self.column, location // self.column

    def __init__(self, row, column, mine_num, todo_tag=False):
        self.row = row
        self.column = column
        self.mine_num = mine_num
        self.matrix = [[self.Cell(self) for _ in range(column)] for _ in range(row)]
        self.todo_tag = todo_tag

        self.swept_num = 0
        self.flagged_mine_num = 0
        self.lose = False

    def __getitem__(self, item):
        x, y = self.split_loc(item)
        return self.matrix[y][x]

    def __len__(self):
        return self.row * self.column

    def win(self):
        return self.swept_num + self.mine_num == self.row * self.column

    def sweep(self, location):
        cell = self[location]

        have_mine = cell.sweep()

        # If this is the first sweep, generate mines after this, so you will not sweep any mines at the first sweep.
        if self.swept_num == 1:
            self.generate_mines()

        # Lose
        if have_mine:
            return self.Lose

        # If sweep a safe cell, expand it.
        if cell.adj_mine_num == 0:
            self.expand(location)

        # Win
        if self.win():
            return self.Win

        # Common
        return self.Common

    def expand(self, location):
        """Explore the map, expand your selection and sweep all safe cells.

        Use BFS.
        """

        visited = [[False for _ in range(self.column)] for _ in range(self.row)]
        q = deque()
        q.append(location)
        visited[location[1]][location[0]] = True

        while q:
            loc = q.popleft()

            for direction in Direction8:
                new_loc = loc[0] + direction[0], loc[1] + direction[1]

                if not self.valid_loc(new_loc):
                    continue
                if visited[new_loc[1]][new_loc[0]]:
                    continue

                visited[new_loc[1]][new_loc[0]] = True
                new_cell = self[new_loc]

                new_cell.sweep()
                if new_cell.adj_mine_num == 0:
                    q.append(new_loc)

    def quick_sweep(self, location):
        """Sweep adjust cells quickly. If all mines around this cell are tagged, it will sweep other cells."""

        cell = self[location]

        if not cell.swept or cell.adj_mine_num == 0:
            return

        adj_no_flag_loc = []
        adj_flag_num = 0
        for direction in Direction8:
            new_loc = location[0] + direction[0], location[1] + direction[1]
            if not self.valid_loc(new_loc):
                continue
            if self[new_loc].tag != self.Cell.Flag:
                adj_no_flag_loc.append(new_loc)
            else:
                adj_flag_num += 1

        # If there are any untagged mines, do nothing.
        if adj_flag_num != cell.adj_mine_num:
            return self.Common

        # Sweep other cells.
        # If you mark wrong mines, you will lose.
        have_mine = False
        for adj_loc in adj_no_flag_loc:
            adj_cell = self[adj_loc]
            have_mine |= adj_cell.sweep()
            if not adj_cell.have_mine and adj_cell.adj_mine_num == 0:
                self.expand(adj_loc)

        if have_mine:
            return self.Lose
        if self.win():
            return self.Win
        return self.Common

    def change_tag(self, location):
        cell = self[location]
        if cell.swept:
            return
        cell.next_tag()

    def reset(self):
        for x in range(self.column):
            for y in range(self.row):
                self[x, y].__init__(self)
        self.swept_num = 0
        self.lose = False

    def generate_mines(self):
        """Generate mines randomly."""

        mine_indices = random.sample([index for index in range(len(self)) if not self[index].swept], self.mine_num)

        for index in mine_indices:
            x, y = index % self.column, index // self.column
            self[x, y].have_mine = True

            # increment adjust cells.
            if x > 0:
                self[x - 1, y].adj_mine_num += 1
                if y > 0:
                    self[x - 1, y - 1].adj_mine_num += 1
                if y < self.row - 1:
                    self[x - 1, y + 1].adj_mine_num += 1
            if x < self.column - 1:
                self[x + 1, y].adj_mine_num += 1
                if y > 0:
                    self[x + 1, y - 1].adj_mine_num += 1
                if y < self.row - 1:
                    self[x + 1, y + 1].adj_mine_num += 1
            if y > 0:
                self[x, y - 1].adj_mine_num += 1
            if y < self.row - 1:
                self[x, y + 1].adj_mine_num += 1

    def valid_loc(self, location):
        x, y = self.split_loc(location)
        return 0 <= x < self.column and 0 <= y < self.row


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

    FontName = 'C:/Windows/Fonts/msyh.ttc'

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
            result = self.state.Common
            events = pygame.event.get()

            for event in events:
                if event.type == pygame.locals.QUIT:
                    running = False
                elif event.type == pygame.locals.KEYDOWN:
                    key_name = get_key_name(event.key, Keymap)

                    if key_name == 'exit':
                        running = False
                    elif key_name == 'restart':
                        self.state.reset()
                        pygame.event.clear()
                    elif key_name == 'sweep':
                        location = self.cell_loc(pygame.mouse.get_pos())
                        if self.state.valid_loc(location):
                            result = self.state.sweep(location)
                    elif key_name == 'quick':
                        location = self.cell_loc(pygame.mouse.get_pos())
                        if self.state.valid_loc(location):
                            result = self.state.quick_sweep(location)
                    elif key_name == 'flag':
                        location = self.cell_loc(pygame.mouse.get_pos())
                        if self.state.valid_loc(location):
                            self.state.change_tag(location)

                elif event.type == pygame.locals.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left key down
                        location = self.cell_loc(event.pos)
                        if self.state.valid_loc(location):
                            result = self.state.sweep(location)
                    elif event.button == 3:  # Right key down
                        location = self.cell_loc(event.pos)
                        if self.state.valid_loc(location):
                            self.state.change_tag(location)
                    elif event.button == 2:  # Middle key down
                        location = self.cell_loc(event.pos)
                        if self.state.valid_loc(location):
                            result = self.state.quick_sweep(location)

            if events:
                self.draw()

            # Test result.
            if result == self.state.Win:
                # Win
                print('You win!')
                pygame.time.delay(1500)
                self.state.reset()
                pygame.event.clear()
            elif result == self.state.Lose:
                # Lose
                print('You lose!')
                self.state.lose = True
                self.draw()
                pygame.time.delay(1500)
                self.state.reset()
                pygame.event.clear()

    def cell_loc(self, physic_loc):
        return (physic_loc[0] - self.top_left_loc[0]) // self.cell_size,\
               (physic_loc[1] - self.top_left_loc[1]) // self.cell_size

    def draw(self):
        self.draw_background()

        # Draw labels.

        # Draw cells.
        for x in range(self.column):
            for y in range(self.row):
                cell = self.state[x, y]

                center_position = (int(self.top_left_loc[0] + (x + 0.5) * self.cell_size),
                                   int(self.top_left_loc[1] + (y + 0.5) * self.cell_size))

                swept_rect = pygame.Rect(
                    self.top_left_loc[0] + x * self.cell_size + self.LineWidth,
                    self.top_left_loc[1] + y * self.cell_size + self.LineWidth,
                    self.cell_size - 2 * self.LineWidth,
                    self.cell_size - 2 * self.LineWidth,
                )

                font = self.get_font(self.FontName, self.cell_size // 2)

                if cell.swept:
                    pygame.draw.rect(self.main_window, self.SweptColor, swept_rect)

                    if cell.have_mine:
                        pygame.draw.circle(self.main_window, self.NumberColors[0],
                                           center_position, int(self.cell_size * 0.4), 0)
                    elif cell.adj_mine_num > 0:
                        text = font.render(str(cell.adj_mine_num), True, self.NumberColors[cell.adj_mine_num], None)
                        text_rect = text.get_rect()
                        text_rect.center = center_position

                        self.main_window.blit(text, text_rect)
                else:
                    pygame.draw.rect(self.main_window, self.UnsweptColor, swept_rect)
                    if self.state.lose and cell.have_mine:
                        pygame.draw.circle(self.main_window, self.NumberColors[0],
                                           center_position, int(self.cell_size * 0.4), 0)
                    else:
                        image_name = None
                        if cell.tag == cell.Flag:
                            image_name = 'flag.png'
                        elif cell.tag == cell.Todo:
                            image_name = 'todo.png'

                        if image_name is not None:
                            image = self.get_image(image_name, (self.cell_size, self.cell_size))
                            image_rect = image.get_rect()
                            image_rect.center = center_position
                            self.main_window.blit(image, image_rect)

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
