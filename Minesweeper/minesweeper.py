# -*- coding: utf-8 -*-

__author__ = 'fyabc'

import random

import pygame
import pygame.locals
from pygame.color import THECOLORS as AllColors
# from pgu import gui

from Utils.basicUtils import getKeyName

SCREEN_SIZE = (750, 750)

FPS = 30
FONT_NAME = 'C:/Windows/Fonts/msyh.ttc'

ROW = 10
COLUMN = 10
MINE_NUM = 25

CELL_SIZE = int(min(SCREEN_SIZE) * 0.7 / max(ROW, COLUMN))
# CELL_SIZE = 60

assert MINE_NUM < ROW * COLUMN

TopLeftLoc = (SCREEN_SIZE[0] // 2 - CELL_SIZE * COLUMN // 2, int(SCREEN_SIZE[1] * 0.6) - CELL_SIZE * ROW // 2)

BG_COLOR = AllColors['gray10']
LINE_COLOR = AllColors['black']
SWEPT_COLOR = AllColors['whitesmoke']
UNSWEPT_COLOR = AllColors['gray30']
# TEXT_COLOR = AllColors['black']

LINE_WIDTH = 1

MainWindow = None
Timer = None

NumberColors = [
    AllColors['black'],     # This is index 0, represents mine.
    AllColors['blue'],
    AllColors['green'],
    AllColors['red'],
    AllColors['brown4'],
    AllColors['lightblue4'],
    AllColors['black'],
    AllColors['gray'],
    AllColors['gray100'],
]

Keymap = {
    'exit': [pygame.locals.K_q, ],
    'restart': [pygame.locals.K_r, ],
}


class GameState:
    FlagImage = None
    TodoImage = None

    class Cell:
        NoTag = 0
        TodoTag = 1
        FlagTag = 2

        def __init__(self, state):
            self.state = state
            self.haveMine = False
            self.adjMineNum = 0
            self.swept = False
            self.tag = self.NoTag

        def sweep(self):
            self.swept = True
            self.tag = self.NoTag
            return self.haveMine

        def changeTag(self, newTag):
            """
            :return: the FlagTag number changed
            """
            result = -(self.tag == self.FlagTag)
            self.tag = newTag
            return result + (self.tag == self.FlagTag)

        def nextTag(self):
            """
            :return: the FlagTag number changed
            """
            result = -(self.tag == self.FlagTag)
            self.tag = (self.tag + 1) % (3 if self.state.todoTag else 2)
            return result + (self.tag == self.FlagTag)

    def __init__(self, row, column, mineNum, todoTag=False):
        self.row = row
        self.column = column
        self.mineNum = mineNum
        self.matrix = [[self.Cell(self) for _ in range(column)] for _ in range(row)]
        self.todoTag = todoTag
        self.sweptNum = 0
        self.flaggedMineNum = 0

    @staticmethod
    def getFlagImage():
        if GameState.FlagImage is None:
            pass
        return GameState.FlagImage

    @staticmethod
    def getTodoImage():
        if GameState.TodoImage is None:
            pass
        return GameState.TodoImage

    def sweep(self, location):
        haveMine = self.getElem(*location).sweep()
        if self.sweptNum == 0:
            self.randomMines()

        self.sweptNum += 1

        if haveMine:
            # Lose
            return -1

        if self.sweptNum + self.mineNum == self.row * self.column:
            # Win
            return 1

        return 0

    def changeTag(self, location):
        cell = self.getElem(*location)
        if cell.swept:
            return
        self.flaggedMineNum += cell.nextTag()

    def reset(self):
        for x in range(self.column):
            for y in range(self.row):
                self.getElem(x, y).__init__()
        self.sweptNum = 0

    def randomMines(self):
        mineLocations = random.sample(
            [index for index in range(self.row * self.column) if (self.getIndex(index).swept is False)],
            self.mineNum)

        for location in mineLocations:
            x, y = location // self.column, location % self.column
            self.getElem(x, y).haveMine = True

            # increment adjust cells.
            if x > 0:
                self.getElem(x - 1, y).adjMineNum += 1
                if y > 0:
                    self.getElem(x - 1, y - 1).adjMineNum += 1
                if y < self.row - 1:
                    self.getElem(x - 1, y + 1).adjMineNum += 1
            if x < self.column - 1:
                self.getElem(x + 1, y).adjMineNum += 1
                if y > 0:
                    self.getElem(x + 1, y - 1).adjMineNum += 1
                if y < self.row - 1:
                    self.getElem(x + 1, y + 1).adjMineNum += 1
            if y > 0:
                self.getElem(x, y - 1).adjMineNum += 1
            if y < self.row - 1:
                self.getElem(x, y + 1).adjMineNum += 1

    def getElem(self, x, y):
        return self.matrix[y][x]

    def getIndex(self, index):
        return self.matrix[index % self.column][index // self.column]

    @staticmethod
    def getLogicLocation(realLocation):
        return (realLocation[0] - TopLeftLoc[0]) // CELL_SIZE, (realLocation[1] - TopLeftLoc[1]) // CELL_SIZE

    def draw(self, surface):
        for x in range(self.column):
            for y in range(self.row):
                cell = self.getElem(x, y)
                sweptRect = pygame.Rect(TopLeftLoc[0] + x * CELL_SIZE + LINE_WIDTH,
                                        TopLeftLoc[1] + y * CELL_SIZE + LINE_WIDTH,
                                        CELL_SIZE - 2 * LINE_WIDTH,
                                        CELL_SIZE - 2 * LINE_WIDTH)
                font = pygame.font.Font(FONT_NAME, CELL_SIZE // 2)

                if cell.swept:
                    centerPosition = (int(TopLeftLoc[0] + (x + 0.5) * CELL_SIZE),
                                      int(TopLeftLoc[1] + (y + 0.5) * CELL_SIZE))
                    pygame.draw.rect(surface, SWEPT_COLOR, sweptRect)

                    if cell.haveMine:
                        pygame.draw.circle(surface, NumberColors[0], centerPosition, int(CELL_SIZE * 0.4), 0)
                    else:
                        if cell.adjMineNum > 0:
                            text = font.render(str(cell.adjMineNum), True,
                                               NumberColors[cell.adjMineNum], None)
                            textRect = text.get_rect()
                            textRect.center = centerPosition
                            surface.blit(text, textRect)
                else:
                    pygame.draw.rect(surface, UNSWEPT_COLOR, sweptRect)
                    if cell.tag == cell.FlagTag:
                        pass
                    elif cell.tag == cell.TodoTag:
                        pass


def drawBackGround():
    MainWindow.fill(BG_COLOR)

    for x in range(COLUMN + 1):
        pygame.draw.line(MainWindow, LINE_COLOR,
                         (TopLeftLoc[0] + x * CELL_SIZE, TopLeftLoc[1]),
                         (TopLeftLoc[0] + x * CELL_SIZE, TopLeftLoc[1] + ROW * CELL_SIZE), LINE_WIDTH)

    for y in range(ROW + 1):
        pygame.draw.line(MainWindow, LINE_COLOR,
                         (TopLeftLoc[0], TopLeftLoc[1] + y * CELL_SIZE),
                         (TopLeftLoc[0] + COLUMN * CELL_SIZE, TopLeftLoc[1] + y * CELL_SIZE), LINE_WIDTH)


def draw(state):
    drawBackGround()

    state.draw(MainWindow)

    pygame.display.update()


def run():
    state = GameState(ROW, COLUMN, MINE_NUM)

    draw(state)

    running = True
    while running:
        Timer.tick(FPS)

        result = 0

        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                running = False
            elif event.type == pygame.locals.KEYDOWN:
                keyName = getKeyName(event.key, Keymap)

                if keyName == 'exit':
                    running = False
            elif event.type == pygame.locals.MOUSEBUTTONDOWN:
                if event.button == 1:       # Left key down
                    result = state.sweep(state.getLogicLocation(event.pos))
                elif event.button == 3:     # Right key down
                    state.changeTag(state.getLogicLocation(event.pos))

        draw(state)

        # Test result.
        if result == 1:
            # Win
            pass
        elif result == -1:
            # Lose
            pass

    pass


def main():
    global MainWindow, Timer

    pygame.init()

    MainWindow = pygame.display.set_mode(SCREEN_SIZE)
    Timer = pygame.time.Clock()

    run()

    pygame.quit()


if __name__ == '__main__':
    main()
