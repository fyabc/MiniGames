# -*- coding: utf-8 -*-

__author__ = 'fyabc'

import random

import pygame
import pygame.locals
from pygame.color import THECOLORS as AllColors

from Utils.basicUtils import getKeyName

FONT_NAME = 'C:/Windows/Fonts/msyh.ttc'

FPS = 30
DEFAULT_SNAKE_LEVEL = 3

ROW = 24
COLUMN = 24

CELL_SIZE = 25
SCREEN_SIZE = (COLUMN * CELL_SIZE + 140, ROW * CELL_SIZE + 140)

TopLeftLoc = (SCREEN_SIZE[0] // 2 - CELL_SIZE * COLUMN // 2, int(SCREEN_SIZE[1] * 0.55) - CELL_SIZE * ROW // 2)

BG_COLOR = AllColors['black']
EDGE_COLOR = AllColors['white']
LINE_COLOR = AllColors['gray18']
SNAKE_COLOR = AllColors['green']
SNAKE_HEAD_COLOR = AllColors['red']
FOOD_COLOR = AllColors['yellow']
TEXT_COLOR = AllColors['white']

LINE_WIDTH = 1

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


class GameState:
    Direction4 = {
        'L': (-1, 0),
        'R': (1, 0),
        'U': (0, -1),
        'D': (0, 1),
    }

    InitLength = 4

    def __init__(self, row, column, foodNum=1, level=DEFAULT_SNAKE_LEVEL):
        self.row = row
        self.column = column
        self.foodNum = foodNum
        self.speed = 3 * level
        assert self.column > 2 * self.InitLength and self.row > 2 * self.InitLength, 'The map is too small'

        self.running = None
        self.length = None
        self.snakeLocs = None
        self.foodLocs = set()
        self.direction = None
        self.score = 0

        self.reset()

    @staticmethod
    def getRealLoc(logicLoc):
        return (TopLeftLoc[0] + int((logicLoc[0] + 0.5) * CELL_SIZE),
                TopLeftLoc[1] + int((logicLoc[1] + 0.5) * CELL_SIZE))

    def generateFood(self, num=1):
        locations = set((x, y) for x in range(self.column) for y in range(self.row))
        locations = locations.difference(self.snakeLocs)
        locations = locations.difference(self.foodLocs)
        return random.sample(locations, num)

    def setSpeedLevel(self, level):
        self.speed = 3 * level

    def getSpeedLevel(self):
        return self.speed // 3

    def updateDirection(self, direction):
        if not self.running:
            return

        if self.direction == direction or\
                (self.direction[0] + direction[0] == 0 and self.direction[1] + direction[1] == 0):
            return
        self.direction = direction

    def isRunning(self):
        return self.running

    def hit(self, location):
        return location[0] < 0 or\
            location[0] >= self.column or\
            location[1] < 0 or\
            location[1] >= self.row or\
            location in self.snakeLocs

    def step(self):
        Timer.tick(self.speed)

        if not self.running:
            return 0

        newSnakeHead = (self.snakeLocs[0][0] + self.direction[0], self.snakeLocs[0][1] + self.direction[1])

        if self.hit(newSnakeHead):
            return -1

        self.snakeLocs.insert(0, newSnakeHead)
        if newSnakeHead in self.foodLocs:
            self.score += self.getSpeedLevel()
            self.foodLocs.remove(newSnakeHead)
            self.foodLocs = self.foodLocs.union(self.generateFood())
        else:
            self.snakeLocs.pop()

        return 0

    def start(self):
        self.running = True

    def pause(self):
        self.running = False

    def reset(self):
        self.running = False
        self.length = self.InitLength
        self.snakeLocs = [(self.column // 2 + i, self.row // 2) for i in range(self.length)]
        self.foodLocs.clear()
        self.foodLocs = self.foodLocs.union(self.generateFood(self.foodNum))
        self.direction = self.Direction4['L']
        self.score = 0

    def draw(self, surface):
        font = pygame.font.Font(FONT_NAME, 25)
        scoreText = font.render('Score: %d' % self.score, True, TEXT_COLOR)
        scoreRect = scoreText.get_rect()
        scoreRect.center = (SCREEN_SIZE[0] * 0.2, SCREEN_SIZE[1] * 0.1)
        speedText = font.render('Speed: %d' % self.getSpeedLevel(), True, TEXT_COLOR)
        speedRect = speedText.get_rect()
        speedRect.center = (SCREEN_SIZE[0] * 0.8, SCREEN_SIZE[1] * 0.1)
        surface.blit(scoreText, scoreRect)
        surface.blit(speedText, speedRect)

        for i, snakeLoc in enumerate(self.snakeLocs):
            centerLoc = self.getRealLoc(snakeLoc)

            rect = pygame.Rect(0, 0, CELL_SIZE, CELL_SIZE)
            rect.center = centerLoc
            pygame.draw.rect(surface, SNAKE_COLOR, rect)
            if i == 0:
                pygame.draw.circle(surface, SNAKE_HEAD_COLOR, centerLoc, int(CELL_SIZE * 0.4))
        for foodLoc in self.foodLocs:
            rect = pygame.Rect(0, 0, CELL_SIZE, CELL_SIZE)
            rect.center = self.getRealLoc(foodLoc)
            pygame.draw.rect(surface, FOOD_COLOR, rect)


def drawBackground():
    MainWindow.fill(BG_COLOR)

    for x in range(COLUMN + 1):
        pygame.draw.line(MainWindow, EDGE_COLOR if x == 0 or x == COLUMN else LINE_COLOR,
                         (TopLeftLoc[0] + x * CELL_SIZE, TopLeftLoc[1]),
                         (TopLeftLoc[0] + x * CELL_SIZE, TopLeftLoc[1] + ROW * CELL_SIZE), LINE_WIDTH)

    for y in range(ROW + 1):
        pygame.draw.line(MainWindow, EDGE_COLOR if y == 0 or y == COLUMN else LINE_COLOR,
                         (TopLeftLoc[0], TopLeftLoc[1] + y * CELL_SIZE),
                         (TopLeftLoc[0] + COLUMN * CELL_SIZE, TopLeftLoc[1] + y * CELL_SIZE), LINE_WIDTH)


def draw(state):
    drawBackground()

    state.draw(MainWindow)

    pygame.display.update()


def run():
    state = GameState(ROW, COLUMN)

    draw(state)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                running = False
            elif event.type == pygame.locals.KEYDOWN:
                keyName = getKeyName(event.key, Keymap)

                if keyName == 'exit':
                    running = False
                elif keyName == 'start':
                    if state.isRunning():
                        state.pause()
                    else:
                        state.start()
                elif keyName == 'pause':
                    state.pause()
                elif keyName == 'reset':
                    state.reset()
                elif keyName == 'left':
                    state.updateDirection(state.Direction4['L'])
                elif keyName == 'right':
                    state.updateDirection(state.Direction4['R'])
                elif keyName == 'up':
                    state.updateDirection(state.Direction4['U'])
                elif keyName == 'down':
                    state.updateDirection(state.Direction4['D'])
                elif keyName is None and 0 < event.key - pygame.locals.K_0 <= 9:
                    if not state.isRunning():
                        state.setSpeedLevel(event.key - pygame.locals.K_0)

        result = state.step()

        if result == -1:    # Lose
            print('You lose!')
            pygame.time.delay(1500)
            state.reset()
            pygame.event.clear()

        draw(state)


def main():
    global MainWindow, Timer

    pygame.init()

    MainWindow = pygame.display.set_mode(SCREEN_SIZE)
    Timer = pygame.time.Clock()

    run()

    pygame.quit()

if __name__ == '__main__':
    main()
