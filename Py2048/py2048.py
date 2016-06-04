# -*- coding: utf-8 -*-

__author__ = 'fyabc'

import random
import json

import pygame
import pygame.locals
from pygame.color import THECOLORS as AllColors

from Py2048.autoGenerators import *
from Utils.basicUtils import getKeyName

SCREEN_SIZE = (750, 700)
FPS = 30
FONT_NAME = 'C:/Windows/Fonts/msyh.ttc'

GENERATE_DELAY = 130
AUTO_GENERATE_DELAY = 60
AUTO_DELAY = 0

MainWindow = None
Timer = None

LoadData = json.load(open('config.json', 'r', encoding='utf-8'))

AllNames = LoadData.get('AllNames') or [
    '2', '4', '8', '16', '32',
    '64', '128', '256', '512', '1024',
    '2048', '4096', '8192', '16384', '32768',
    '65536', '131072', '262144', '524288', '1048576',
    '2097152', '4194304', '8388608', '16777216', '33554432',
    '67108864', '134217728',
]

NameColors = LoadData.get('NameColors') or [
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

CELL_SIZE = 100

COLUMN = 4
ROW = 4

TopLeftLoc = (SCREEN_SIZE[0] // 2 - CELL_SIZE * COLUMN // 2, SCREEN_SIZE[1] // 2 - CELL_SIZE * ROW // 2)

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

BG_COLOR = AllColors['white']
LINE_COLOR = AllColors['blue']
TEXT_COLOR = AllColors['black']


class GameState:
    """
    [NOTE]: The (x, y) in state means the x-th column and the y-th row.
            In other word, x is the x-coordinate, y is the y-coordinate.
    """
    PROBABILITY_0 = 0.9     # The probability of 0, the probability of 1 is (1 - PROBABILITY_0)

    def __init__(self, row, column, autoType=0):
        self.matrix = [[-1 for _ in range(column)] for _ in range(row)]
        self.row = row
        self.column = column
        self.score = 0
        self.autoType = autoType

    def getElem(self, x, y):
        return self.matrix[y][x]

    def setElem(self, x, y, value):
        self.matrix[y][x] = value

    def randLoc(self):
        empties = []
        for x in range(self.column):
            for y in range(self.row):
                if self.getElem(x, y) == -1:
                    empties.append((x, y))
        if len(empties) == 0:
            return None
        return random.choice(empties)

    def generate(self):
        loc = self.randLoc()
        if loc is None:
            return False

        value = 0 if random.random() < self.PROBABILITY_0 else 1
        self.setElem(*loc, value)

        return True

    def reset(self):
        self.score = 0

        for x in range(self.column):
            for y in range(self.row):
                self.setElem(x, y, -1)

        self.generate()
        self.generate()

    def dead(self):
        for x in range(self.column):
            for y in range(self.row):
                if self.getElem(x, y) == -1:
                    return False
                if x < self.column - 1 and self.getElem(x, y) == self.getElem(x + 1, y):
                    return False
                if y < self.row - 1 and self.getElem(x, y) == self.getElem(x, y + 1):
                    return False
        return True

    def up(self):
        moved = 0

        for y in range(self.row):
            for x in range(self.column):
                value = self.getElem(x, y)

                if value == -1:
                    continue

                newY = y
                while newY > 0 and self.getElem(x, newY - 1) == -1:
                    newY -= 1

                self.setElem(x, y, -1)

                if newY > 0 and self.getElem(x, newY - 1) == value:
                    # merge
                    self.setElem(x, newY - 1, value + 1)
                    self.score += (4 << value)
                    newY -= 1
                else:
                    # not merge
                    self.setElem(x, newY, value)

                if newY != y:
                    moved += 1

        return moved

    def down(self):
        moved = 0

        for y in reversed(range(self.row)):
            for x in range(self.column):
                value = self.getElem(x, y)

                if value == -1:
                    continue

                newY = y
                while newY < self.row - 1 and self.getElem(x, newY + 1) == -1:
                    newY += 1

                self.setElem(x, y, -1)

                if newY < self.row - 1 and self.getElem(x, newY + 1) == value:
                    # merge
                    self.setElem(x, newY + 1, value + 1)
                    self.score += (4 << value)
                    newY += 1
                else:
                    # not merge
                    self.setElem(x, newY, value)

                if newY != y:
                    moved += 1

        return moved

    def left(self):
        moved = 0

        for x in range(self.column):
            for y in range(self.row):
                value = self.getElem(x, y)

                if value == -1:
                    continue

                newX = x
                while newX > 0 and self.getElem(newX - 1, y) == -1:
                    newX -= 1

                self.setElem(x, y, -1)

                if newX > 0 and self.getElem(newX - 1, y) == value:
                    # merge
                    self.setElem(newX - 1, y, value + 1)
                    self.score += (4 << value)
                    newX -= 1
                else:
                    # not merge
                    self.setElem(newX, y, value)

                if newX != x:
                    moved += 1

        return moved

    def right(self):
        moved = 0

        for x in reversed(range(self.column)):
            for y in range(self.row):
                value = self.getElem(x, y)

                if value == -1:
                    continue

                newX = x
                while newX < self.column - 1 and self.getElem(newX + 1, y) == -1:
                    newX += 1

                self.setElem(x, y, -1)

                if newX < self.column - 1 and self.getElem(newX + 1, y) == value:
                    # merge
                    self.setElem(newX + 1, y, value + 1)
                    self.score += (4 << value)
                    newX += 1
                else:
                    # not merge
                    self.setElem(newX, y, value)

                if newX != x:
                    moved += 1

        return moved

    def draw(self, surface):
        font = pygame.font.Font(FONT_NAME, CELL_SIZE // 2)

        for x in range(self.column):
            for y in range(self.row):
                value = self.getElem(x, y)
                if value != -1:
                    cellRect = pygame.Rect(0, 0, int(CELL_SIZE * 0.8), int(CELL_SIZE * 0.8))
                    cellRect.center = (TopLeftLoc[0] + (x + 0.5) * CELL_SIZE, TopLeftLoc[1] + (y + 0.5) * CELL_SIZE)

                    pygame.draw.rect(surface, NameColors[value], cellRect, 0)
                    text = font.render(AllNames[value], True, AllColors['white'], None)
                    textRect = text.get_rect()
                    textRect.center = cellRect.center
                    surface.blit(text, textRect)


def drawBackGround():
    MainWindow.fill(BG_COLOR)

    for x in range(COLUMN + 1):
        pygame.draw.line(MainWindow, LINE_COLOR,
                         (TopLeftLoc[0] + x * CELL_SIZE, TopLeftLoc[1]),
                         (TopLeftLoc[0] + x * CELL_SIZE, TopLeftLoc[1] + ROW * CELL_SIZE), 4)

    for y in range(ROW + 1):
        pygame.draw.line(MainWindow, LINE_COLOR,
                         (TopLeftLoc[0], TopLeftLoc[1] + y * CELL_SIZE),
                         (TopLeftLoc[0] + COLUMN * CELL_SIZE, TopLeftLoc[1] + y * CELL_SIZE), 4)


def draw(state):
    drawBackGround()

    font = pygame.font.Font(FONT_NAME, 50)
    scoreText = font.render('Score: %d' % state.score, True, TEXT_COLOR)
    scoreTextRect = scoreText.get_rect()
    scoreTextRect.center = (SCREEN_SIZE[0] * 0.5, SCREEN_SIZE[1] * 0.1)

    MainWindow.blit(scoreText, scoreTextRect)

    state.draw(MainWindow)

    pygame.display.update()


def run():
    state = GameState(ROW, COLUMN)
    state.reset()

    # initialize some auto iterators.
    rotateIter = rotateAuto2(state)
    LDRDIter = DRDLAuto(state)
    cornerIter = cornerAuto(state)

    next(rotateIter)
    next(LDRDIter)
    next(cornerIter)

    draw(state)

    moved = 1

    running = True
    while running:
        Timer.tick(FPS)

        if state.autoType == 0:
            moved = 0

            for event in pygame.event.get():
                if event.type == pygame.locals.QUIT:
                    running = False
                elif event.type == pygame.locals.KEYDOWN:
                    keyName = getKeyName(event.key, Keymap)

                    if keyName == 'exit':
                        running = False
                    elif keyName == 'reset':
                        state.reset()
                    elif keyName == 'up':
                        moved = state.up()
                    elif keyName == 'down':
                        moved = state.down()
                    elif keyName == 'left':
                        moved = state.left()
                    elif keyName == 'right':
                        moved = state.right()
                    elif keyName == 'auto':
                        state.autoType = event.key - pygame.locals.K_0

        else:
            autoIter = rotateIter
            if state.autoType == 1:
                autoIter = rotateIter
            elif state.autoType == 2:
                autoIter = LDRDIter
            elif state.autoType == 3:
                autoIter = cornerIter

            pygame.time.delay(AUTO_DELAY)
            moved = (autoIter.send(moved))()

            for event in pygame.event.get():
                if event.type == pygame.locals.QUIT:
                    running = False
                elif event.type == pygame.locals.KEYDOWN:
                    keyName = getKeyName(event.key, Keymap)

                    if keyName == 'exit':
                        running = False
                    elif keyName == 'reset':
                        state.reset()
                    elif keyName == 'auto':
                        state.autoType = event.key - pygame.locals.K_0
                    elif keyName == 'manual':
                        state.autoType = 0

        draw(state)
        if moved > 0:
            pygame.time.delay(GENERATE_DELAY if state.autoType == 0 else AUTO_GENERATE_DELAY)
            state.generate()
            draw(state)

        if state.dead():
            text = pygame.font.Font(FONT_NAME, 70).render('You Lose!', True, AllColors['blueviolet'], None)
            textRect = text.get_rect()
            textRect.center = (SCREEN_SIZE[0] / 2, SCREEN_SIZE[1] / 2)

            MainWindow.blit(text, textRect)
            pygame.display.update()

            pygame.time.delay(1500)

            state.reset()


def main():
    global MainWindow, Timer

    pygame.init()

    MainWindow = pygame.display.set_mode(SCREEN_SIZE)
    Timer = pygame.time.Clock()

    pygame.event.set_blocked(
        (pygame.locals.MOUSEBUTTONDOWN,
         pygame.locals.MOUSEBUTTONUP,
         pygame.locals.MOUSEMOTION,
         pygame.locals.KEYUP,
         )
    )

    run()

    pygame.quit()

if __name__ == '__main__':
    main()
