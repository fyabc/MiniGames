#! /usr/bin/python
# -*- encoding: utf-8 -*-

import random
import argparse

import pygame
import pygame.locals

from ..basic.runner import PygameRunner
from ..utils.constant import Colors, FPS
from ..utils.basic import get_key_name, parse_size
from ..utils.arguments import arg_size

__author__ = 'fyabc'


GameName = 'Snake'

AllowEvents = (pygame.locals.QUIT, pygame.locals.KEYDOWN,)

DefaultRow = 24
DefaultColumn = 24
DefaultInitLength = 4

MinRow = 5
MinColumn = 5


Keymap = {
    'exit': [pygame.locals.K_q, ],
    'start': [pygame.locals.K_s, ],
    'pause': [pygame.locals.K_p, ],
    'reset': [pygame.locals.K_r, ],
    'left': [pygame.locals.K_LEFT, ],
    'right': [pygame.locals.K_RIGHT, ],
    'up': [pygame.locals.K_UP, ],
    'down': [pygame.locals.K_DOWN, ],
}


class GameState:
    Direction4 = {
        'L': (-1, 0),
        'R': (1, 0),
        'U': (0, -1),
        'D': (0, 1),
    }

    Win = 1
    Lose = -1
    Common = 0

    DefaultFoodNumber = 1
    DefaultInitLength = 4
    DefaultLevel = 3

    def __init__(self, column, row, **kwargs):
        self.column = column
        self.row = row
        self.init_length = kwargs.pop('init_length', self.DefaultInitLength)

        assert self.column > 2 * self.init_length and self.row > 2 * self.init_length, 'The map is too small'

        self.food_num = kwargs.pop('food_num', self.DefaultFoodNumber)
        self.length = None
        self.snake_loc = None
        self.food_loc = set()
        self.direction = None
        self.score = 0
        self.level = kwargs.pop('level', self.DefaultLevel)

        self.reset()

    @property
    def speed(self):
        return 3 * self.level

    def reset(self):
        self.length = self.init_length
        self.snake_loc = [(self.column // 2 + i, self.row // 2) for i in range(self.length)]
        self.food_loc.clear()
        self.food_loc |= self.generate_food(self.food_num)
        self.direction = self.Direction4['L']
        self.score = 0

    def step(self):
        new_snake_head = self.snake_loc[0][0] + self.direction[0], self.snake_loc[0][1] + self.direction[1]

        if self.hit(new_snake_head):
            return self.Lose

        self.snake_loc.insert(0, new_snake_head)
        if new_snake_head in self.food_loc:
            self.score += self.level
            self.food_loc.remove(new_snake_head)
            self.food_loc |= self.generate_food()
        else:
            self.snake_loc.pop()

        return self.Common

    def hit(self, location):
        return location[0] < 0 or \
               location[0] >= self.column or \
               location[1] < 0 or \
               location[1] >= self.row or \
               location in self.snake_loc

    def generate_food(self, food_num=1):
        locations = set((x, y) for x in range(self.column) for y in range(self.row))\
                    - self.food_loc - set(self.snake_loc)
        return set(random.sample(locations, food_num))
    
    def update_direction(self, new_direction):
        if self.direction[0] + new_direction[0] == 0 and self.direction[1] + new_direction[1] == 0:
            return 
        self.direction = new_direction


class Snake(PygameRunner):
    # Some color and style constants.
    BGColor = Colors['black']
    EdgeColor = Colors['white']
    LineColor = Colors['gray18']
    SnakeColor = Colors['green']
    SnakeHeadColor = Colors['red']
    FoodColor = Colors['yellow']
    TextColor = Colors['white']
    
    LineWidth = 1

    FontName = 'C:/Windows/Fonts/msyh.ttc'
    FontSize = 25

    CellSize = 25

    FPS = 30

    def __init__(self, **kwargs):
        self.row = max(kwargs.pop('row', DefaultRow), MinRow)
        self.column = max(kwargs.pop('column', DefaultColumn), MinColumn)

        super().__init__(
            screen_size=(self.column * self.CellSize + 140, self.row * self.CellSize + 140),
            name=GameName,
            allow_events=AllowEvents,
        )

        self.top_left_loc = (self.screen_size[0] // 2 - self.CellSize * self.column // 2,
                             int(self.screen_size[1] * 0.55) - self.CellSize * self.row // 2)

        self.state = GameState(self.column, self.row, **kwargs)
        self.running = False

    def step(self):
        self.timer.tick(self.state.speed)

        if not self.running:
            return self.state.Common

        return self.state.step()

    def physic_loc(self, logic_loc):
        return self.top_left_loc[0] + int((logic_loc[0] + 0.5) * self.CellSize),\
               self.top_left_loc[1] + int((logic_loc[1] + 0.5) * self.CellSize)
    
    def main_loop(self):
        self.draw()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.locals.QUIT:
                    running = False
                elif event.type == pygame.locals.KEYDOWN:
                    key_name = get_key_name(event.key, Keymap)

                    if key_name == 'exit':
                        running = False
                    elif key_name == 'start':
                        self.running = not self.running
                    elif key_name == 'pause':
                        self.running = False
                    elif key_name == 'reset':
                        self.state.reset()
                    elif key_name == 'left':
                        self.state.update_direction(self.state.Direction4['L'])
                    elif key_name == 'right':
                        self.state.update_direction(self.state.Direction4['R'])
                    elif key_name == 'up':
                        self.state.update_direction(self.state.Direction4['U'])
                    elif key_name == 'down':
                        self.state.update_direction(self.state.Direction4['D'])
                    elif key_name is None and 0 < event.key - pygame.locals.K_0 <= 9:
                        if not self.running:
                            self.state.level = event.key - pygame.locals.K_0

            result = self.step()

            if result == self.state.Lose:
                print('You lose!')
                pygame.time.delay(1500)
                self.state.reset()
                pygame.event.clear()

            self.draw()

    def draw(self):
        self.draw_background()

        font = self.get_font(self.FontName, self.FontSize)

        score_text = font.render('Score: {}'.format(self.state.score), True, self.TextColor)
        score_rect = score_text.get_rect()
        score_rect.center = self.screen_size[0] * 0.2, self.screen_size[1] * 0.1
        self.main_window.blit(score_text, score_rect)

        speed_text = font.render('Speed: {}'.format(self.state.level), True, self.TextColor)
        speed_rect = speed_text.get_rect()
        speed_rect.center = self.screen_size[0] * 0.8, self.screen_size[1] * 0.1
        self.main_window.blit(speed_text, speed_rect)

        # Draw snake
        for i, snake_loc in enumerate(self.state.snake_loc):
            center_loc = self.physic_loc(snake_loc)

            rect = pygame.Rect(0, 0, self.CellSize, self.CellSize)
            rect.center = center_loc
            pygame.draw.rect(self.main_window, self.SnakeColor, rect)

            # Draw head
            if i == 0:
                pygame.draw.circle(self.main_window, self.SnakeHeadColor, center_loc, int(self.CellSize * 0.4))

        # Draw food
        for food_loc in self.state.food_loc:
            rect = pygame.Rect(0, 0, self.CellSize, self.CellSize)
            rect.center = self.physic_loc(food_loc)
            pygame.draw.rect(self.main_window, self.FoodColor, rect)

        pygame.display.update()

    def draw_background(self):
        self.main_window.fill(self.BGColor)

        for x in range(self.column + 1):
            pygame.draw.line(
                self.main_window, self.EdgeColor if x == 0 or x == self.row else self.LineColor,
                (self.top_left_loc[0] + x * self.CellSize, self.top_left_loc[1]),
                (self.top_left_loc[0] + x * self.CellSize, self.top_left_loc[1] + self.row * self.CellSize),
                self.LineWidth,
            )

        for y in range(self.row + 1):
            pygame.draw.line(
                self.main_window, self.EdgeColor if y == 0 or y == self.column else self.LineColor,
                (self.top_left_loc[0], self.top_left_loc[1] + y * self.CellSize),
                (self.top_left_loc[0] + self.column * self.CellSize, self.top_left_loc[1] + y * self.CellSize),
                self.LineWidth,
            )


def real_main(options):
    row, column = parse_size(options.size)

    game = Snake(row=row, column=column, level=options.level, food_num=options.food_num)

    game.run()


def build_parser():
    parser = argparse.ArgumentParser(prog='snake', description='A simple implementation of Snake.')

    arg_size(parser, default='24x24', help='The size of the map, format is "axb", default is "24x24" '
                                           '(a must >= {}, b must >= {}).'.format(MinRow, MinColumn))
    parser.add_argument('-l', '--level', metavar='N', dest='level', default=GameState.DefaultLevel, type=int,
                        help='The speed level, default is {}'.format(GameState.DefaultLevel))
    parser.add_argument('-f', '--food', metavar='N', dest='food_num', default=GameState.DefaultFoodNumber, type=int,
                        help='The food number default is {}'.format(GameState.DefaultFoodNumber))

    return parser


def main():
    parser = build_parser()

    options = parser.parse_args()

    real_main(options)
