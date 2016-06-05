# -*- coding: utf-8 -*-

__author__ = 'fyabc'

import random
import os
import queue

import pygame
import pygame.locals
from pygame.color import THECOLORS as AllColors

from Utils.basicUtils import getKeyName

FPS = 50
FONT_NAME = 'C:/Windows/Fonts/msyh.ttc'

ROW = 15
COLUMN = 30
MINE_NUM = 99

SCREEN_SIZE = (COLUMN * 45, ROW * 45)
CELL_SIZE = int(min([SCREEN_SIZE[0] / COLUMN, SCREEN_SIZE[1] / ROW]) * 0.8)
# CELL_SIZE = 60

assert MINE_NUM < ROW * COLUMN

TopLeftLoc = (SCREEN_SIZE[0] // 2 - CELL_SIZE * COLUMN // 2, int(SCREEN_SIZE[1] * 0.55) - CELL_SIZE * ROW // 2)

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
    'sweep': [pygame.locals.K_s, ],
    'flag': [pygame.locals.K_f, ],
    'quick': [pygame.locals.K_k, ],
}

Direction8 = (
    (1, 0), (-1, 0), (0, 1), (0, -1),
    (1, 1), (1, -1), (-1, 1), (-1, -1)
)


class GameState:
    FlagImage = None
    TodoImage = None

    class Cell:
        NoTag = 0
        FlagTag = 1
        TodoTag = 2

        def __init__(self, state):
            self.state = state
            self.haveMine = False
            self.adjMineNum = 0
            self.swept = False
            self.tag = self.NoTag

        def sweep(self):
            if self.swept:
                return False

            self.state.sweptNum += 1
            self.swept = True
            self.tag = self.NoTag

            if self.tag == self.FlagTag:
                self.state.flaggedMineNum -= 1
            return self.haveMine

        def changeTag(self, newTag):
            if self.tag == self.FlagTag:
                self.state.flaggedMineNum -= 1
            self.tag = newTag
            if self.tag == self.FlagTag:
                self.state.flaggedMineNum += 1

        def nextTag(self):
            if self.tag == self.FlagTag:
                self.state.flaggedMineNum -= 1
            self.tag = (self.tag + 1) % (3 if self.state.todoTag else 2)
            if self.tag == self.FlagTag:
                self.state.flaggedMineNum += 1

    def __init__(self, row, column, mineNum, todoTag=False):
        self.row = row
        self.column = column
        self.mineNum = mineNum
        self.matrix = [[self.Cell(self) for _ in range(column)] for _ in range(row)]
        self.todoTag = todoTag
        self.sweptNum = 0
        self.flaggedMineNum = 0
        self.lose = False

    @staticmethod
    def getFlagImage():
        if GameState.FlagImage is None:
            GameState.FlagImage = pygame.transform.scale(
                pygame.image.load(os.path.join(os.sep, os.path.dirname(__file__), 'resource', 'flag.png')
                                  ).convert_alpha(),
                (CELL_SIZE, CELL_SIZE))
        return GameState.FlagImage

    @staticmethod
    def getTodoImage():
        if GameState.TodoImage is None:
            GameState.TodoImage = pygame.transform.scale(
                pygame.image.load(os.path.join(os.sep, os.path.dirname(__file__), 'resource', 'todo.png')
                                  ).convert_alpha(),
                (CELL_SIZE, CELL_SIZE))
        return GameState.TodoImage

    def win(self):
        return self.sweptNum + self.mineNum == self.row * self.column

    def sweep(self, location):
        cell = self.getElem(*location)
        haveMine = cell.sweep()

        if self.sweptNum == 1:
            self.randomMines()

        if haveMine:    # Lose
            return -1

        if cell.adjMineNum == 0:
            self.expand(location)

        if self.win():  # Win
            return 1

        return 0

    def expand(self, location):
        visited = [[False for _ in range(self.column)] for _ in range(self.row)]
        q = queue.Queue()
        q.put(location, block=False)
        visited[location[1]][location[0]] = True

        while not q.empty():
            loc = q.get(block=False)

            for direction in Direction8:
                newLoc = (loc[0] + direction[0], loc[1] + direction[1])
                if newLoc[0] < 0 or newLoc[0] >= self.column or newLoc[1] < 0 or newLoc[1] >= self.row:
                    continue
                if visited[newLoc[1]][newLoc[0]]:
                    continue

                visited[newLoc[1]][newLoc[0]] = True
                newCell = self.getElem(*newLoc)

                newCell.sweep()
                if newCell.adjMineNum == 0:
                    q.put(newLoc, block=False)

    def quickSweep(self, location):
        cell = self.getElem(*location)
        if not cell.swept or cell.adjMineNum == 0:
            return 0

        adjNoFlagLoc = []
        adjFlagNum = 0
        for direction in Direction8:
            newLoc = (location[0] + direction[0], location[1] + direction[1])
            if newLoc[0] < 0 or newLoc[0] >= self.column or newLoc[1] < 0 or newLoc[1] >= self.row:
                continue
            if self.getElem(*newLoc).tag != self.Cell.FlagTag:
                adjNoFlagLoc.append(newLoc)
            else:
                adjFlagNum += 1

        if adjFlagNum != cell.adjMineNum:
            return 0

        haveMine = False
        for adjLoc in adjNoFlagLoc:
            adjCell = self.getElem(*adjLoc)
            haveMine |= adjCell.sweep()
            if not adjCell.haveMine and adjCell.adjMineNum == 0:
                self.expand(adjLoc)

        if haveMine:
            return -1
        if self.win():
            return 1
        return 0

    def changeTag(self, location):
        cell = self.getElem(*location)
        if cell.swept:
            return
        cell.nextTag()

    def reset(self):
        for x in range(self.column):
            for y in range(self.row):
                self.getElem(x, y).__init__(self)
        self.sweptNum = 0
        self.lose = False

    def randomMines(self):
        mineIndexes = random.sample(
            [index for index in range(self.row * self.column) if (self.getIndex(index).swept is False)],
            self.mineNum)

        for index in mineIndexes:
            x, y = index % self.column, index // self.column
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
        return self.matrix[index // self.column][index % self.column]

    def validLocation(self, location):
        return 0 <= location[0] < self.column and 0 <= location[1] < self.row

    @staticmethod
    def getLogicLocation(realLocation):
        return (realLocation[0] - TopLeftLoc[0]) // CELL_SIZE, (realLocation[1] - TopLeftLoc[1]) // CELL_SIZE

    def draw(self, surface):
        # Draw labels.

        # Draw cells.
        for x in range(self.column):
            for y in range(self.row):
                cell = self.getElem(x, y)
                centerPosition = (int(TopLeftLoc[0] + (x + 0.5) * CELL_SIZE),
                                  int(TopLeftLoc[1] + (y + 0.5) * CELL_SIZE))
                sweptRect = pygame.Rect(TopLeftLoc[0] + x * CELL_SIZE + LINE_WIDTH,
                                        TopLeftLoc[1] + y * CELL_SIZE + LINE_WIDTH,
                                        CELL_SIZE - 2 * LINE_WIDTH,
                                        CELL_SIZE - 2 * LINE_WIDTH)
                font = pygame.font.Font(FONT_NAME, CELL_SIZE // 2)

                if cell.swept:
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
                    if self.lose and cell.haveMine:
                        pygame.draw.circle(surface, NumberColors[0], centerPosition, int(CELL_SIZE * 0.4), 0)
                    elif cell.tag == cell.FlagTag:
                        flagImage = self.getFlagImage()
                        flagRect = flagImage.get_rect()
                        flagRect.center = centerPosition
                        surface.blit(flagImage, flagRect)
                    elif cell.tag == cell.TodoTag:
                        todoImage = self.getTodoImage()
                        todoRect = todoImage.get_rect()
                        todoRect.center = centerPosition
                        surface.blit(todoImage, todoRect)


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
        # Timer.tick(FPS)

        result = 0
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.locals.QUIT:
                running = False
            elif event.type == pygame.locals.KEYDOWN:
                keyName = getKeyName(event.key, Keymap)

                if keyName == 'exit':
                    running = False
                elif keyName == 'restart':
                    state.reset()
                    pygame.event.clear()
                elif keyName == 'sweep':
                    location = state.getLogicLocation(pygame.mouse.get_pos())
                    if state.validLocation(location):
                        result = state.sweep(location)
                elif keyName == 'quick':
                    location = state.getLogicLocation(pygame.mouse.get_pos())
                    if state.validLocation(location):
                        result = state.quickSweep(location)
                elif keyName == 'flag':
                    location = state.getLogicLocation(pygame.mouse.get_pos())
                    if state.validLocation(location):
                        state.changeTag(location)

            elif event.type == pygame.locals.MOUSEBUTTONDOWN:
                if event.button == 1:       # Left key down
                    location = state.getLogicLocation(event.pos)
                    if state.validLocation(location):
                        result = state.sweep(location)
                elif event.button == 3:     # Right key down
                    location = state.getLogicLocation(event.pos)
                    if state.validLocation(location):
                        state.changeTag(location)
                elif event.button == 2:     # Middle key down
                    location = state.getLogicLocation(event.pos)
                    if state.validLocation(location):
                        result = state.quickSweep(location)

        if len(events) > 0:
            draw(state)

        # Test result.
        if result == 1:
            # Win
            print('You win!')
            pygame.time.delay(1500)
            state.reset()
            pygame.event.clear()
        elif result == -1:
            # Lose
            print('You lose!')
            state.lose = True
            draw(state)
            pygame.time.delay(1500)
            state.reset()
            pygame.event.clear()


def main():
    global MainWindow, Timer

    pygame.init()

    MainWindow = pygame.display.set_mode(SCREEN_SIZE)
    Timer = pygame.time.Clock()

    pygame.event.set_allowed([
        pygame.locals.QUIT,
        pygame.locals.MOUSEBUTTONDOWN,
        pygame.locals.KEYDOWN,
    ])

    run()

    pygame.quit()


if __name__ == '__main__':
    main()
