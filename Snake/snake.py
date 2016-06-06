# -*- coding: utf-8 -*-

__author__ = 'fyabc'

import pygame
import pygame.locals
from pygame.color import THECOLORS as AllColors


FONT_NAME = 'C:/Windows/Fonts/msyh.ttc'

FPS = 30

ROW = 25
COLUMN = 35

CELL_SIZE = 20
SCREEN_SIZE = (COLUMN * CELL_SIZE + 140, ROW * CELL_SIZE + 140)

TopLeftLoc = (SCREEN_SIZE[0] // 2 - CELL_SIZE * COLUMN // 2, int(SCREEN_SIZE[1] * 0.55) - CELL_SIZE * ROW // 2)

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

MainWindow = None
Timer = None

Direction4 = (
    (1, 0),
    (-1, 0),
    (0, 1),
    (0, -1),
)


class GameState:
    InitLength = 4

    def __init__(self, row, column):
        self.row = row
        self.column = column
        self.running = False
        self.length = self.InitLength
        self.snakeLoc = None
        self.foodLocs = None

    def start(self):
        self.running = True

    def pause(self):
        self.running = False

    def reset(self):
        self.running = False
        self.length = self.InitLength
        self.snakeLoc = None


def drawBackground():
    pass


def draw(state):
    pass


def run():

    running = True
    while running:
        Timer.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                running = False


def main():
    global MainWindow, Timer

    pygame.init()

    MainWindow = pygame.display.set_mode(SCREEN_SIZE)
    Timer = pygame.time.Clock()

    run()

    pygame.quit()

if __name__ == '__main__':
    main()
