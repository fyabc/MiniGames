# -*- coding: utf-8 -*-

__author__ = 'fyabc'

import os
from random import randint

import pygame

from Utils.vector2 import Vector2
from StateMachine.simpleBrain import Brain
from AntsSpiders.config import *
from AntsSpiders.states import AntExploring, AntSeeking, AntDelivering, AntHunting


def getPath(*paths):
    return os.path.join(os.sep, os.path.dirname(__file__), *paths)


class World:
    def __init__(self):
        self.entities = {}
        self.nextEntityID = 0

    def addEntity(self, newEntity):
        self.entities[self.nextEntityID] = newEntity
        newEntity.id = self.nextEntityID
        newEntity.world = self
        newEntity.valid = True
        self.nextEntityID += 1

    def removeEntity(self, entity):
        del self.entities[entity.id]

    def getEntity(self, entityID):
        if entityID in self.entities:
            return self.entities[entityID]
        else:
            return None

    def drawBackground(self, surface):
        surface.fill(BG_COLOR)

    def draw(self, surface: pygame.Surface):
        self.drawBackground(surface)
        for entity in self.entities.values():
            if entity.valid:
                entity.draw(surface)

    def step(self, timePassed):
        # You cannot delete an entity when iterating entities, so add its id into lostEntities,
        # then remove them after iteration.

        lostEntities = set()
        for entity in self.entities.values():
            if entity.valid:
                entity.step(timePassed)
                if not entity.valid:
                    lostEntities.add(entity.id)
            else:
                # if not valid, not iterate it.
                lostEntities.add(entity.id)

        # remove all invalid entities.
        self_entities = self.entities   # This is to speed up.
        for entityId in lostEntities:
            del self_entities[entityId]

    def getCloseEntity(self, name, location, seeRange=100.):
        locationVec = Vector2(*location)
        for entity in self.entities.values():
            if entity.valid and entity.name == name:
                distance = locationVec.distance(entity.location)
                if distance < seeRange:
                    return entity
        return None


class WorldEntity:
    DefaultFont = None

    def __init__(self, name, world=None):
        self.name = name
        self.world = world
        self.id = None
        self.valid = True

        if self.world is not None:
            self.world.addEntity(self)

        w, h = SCREEN_SIZE
        self.location = Vector2(randint(0, w), randint(0, h))
        self.destination = Vector2(randint(0, w), randint(0, h))
        self.speed = 0.

        self.brain = Brain()
        self.image = None

    @staticmethod
    def getFont():
        if WorldEntity.DefaultFont is None:
            WorldEntity.DefaultFont = pygame.font.SysFont(None, 8)
        return WorldEntity.DefaultFont

    def __str__(self):
        return "('%s', %d)" % (self.name, self.id)

    def __repr__(self):
        return "WorldEntity(name='%s', id=%d)" % (self.name, self.id)

    def invalidate(self):
        # invalidate an entity do not delete from self.entities, just set in into invalid.
        self.world = None
        self.valid = False

    def draw(self, surface: pygame.Surface):
        x, y = self.location
        w, h = self.image.get_size()
        surface.blit(self.image, (x - w / 2, y - h / 2))

    def step(self, timePassed):     # timePassed为一步时间间隔
        self.brain.think()          # 通过状态机改变该物体的destination和speed等状态（先doAction，再checkCond，最后移动）

        if self.speed > 0 and self.location != self.destination:
            tempVec = self.destination - self.location                      # 从起点到终点的向量
            distance = min(tempVec.length, timePassed * self.speed)         # 应该移动的距离
            tempVec.normalize()                                             # 从起点到终点的单位向量
            self.location += distance * tempVec                             # 新位置


class AntsSpidersWorld(World):
    def __init__(self):
        super(AntsSpidersWorld, self).__init__()
        self.background = pygame.Surface(SCREEN_SIZE).convert()
        self.background.fill(BG_COLOR)
        pygame.draw.circle(self.background, NEST_COLOR, NEST_LOC, NEST_RADIUS)

    def drawBackground(self, surface):
        surface.blit(self.background, (0, 0))

    def clearDeath(self, surface):
        # 清除所有树叶和死掉的蜘蛛
        print('巢穴里的蚂蚁清理掉了所有树叶和死掉的蜘蛛！')

        self.background.fill(BG_COLOR)
        pygame.draw.circle(self.background, NEST_COLOR, NEST_LOC, NEST_RADIUS)
        surface.blit(self.background, (0, 0))


class Leaf(WorldEntity):
    Image = None

    @staticmethod
    def loadImage():
        if Leaf.Image is None:
            Leaf.Image = pygame.image.load(getPath('resource', 'leaf.jpg')).convert_alpha()
            Leaf.Image = pygame.transform.scale(Leaf.Image, (24, 16))
        return Leaf.Image

    def __init__(self, world=None):
        super(Leaf, self).__init__('leaf', world)
        self.image = self.loadImage()


class Spider(WorldEntity):
    Image = None

    MaxLevel = 5  # 满级

    @staticmethod
    def loadImage():
        if Spider.Image is None:
            Spider.Image = pygame.image.load(getPath('resource', 'spider.jpg')).convert_alpha()
            Spider.Image = pygame.transform.scale(Spider.Image, (36, 24))
        return Spider.Image

    def __init__(self, world=None):
        super(Spider, self).__init__('spider', world)
        self.image = self.loadImage()
        self.alive = True
        self.levelIter = self.nextLevel()
        self.level, self.maxHp, self.attack, self.nextExp = next(self.levelIter)
        self.hp = self.maxHp
        self.speed = randint(*SPIDER_SPEED_RANGE)
        self.exp = 0

    def died(self):
        if self.alive:
            print('%d号%s死亡了！' % (self.id, self.name))
            self.alive = False
            # 用一个翻过来的图片代表一个死掉的蜘蛛
            self.image = pygame.transform.flip(self.image, 0, 1)
            self.speed = 0.

    def attacked(self, attacker):
        print('%d号%s受到了%d号%s的攻击！' % (self.id, self.name, attacker.id, attacker.name))
        self.hp -= attacker.attack * 1
        if self.hp <= 0:
            self.died()
            return
        self.exp += attacker.level * 1  # 战斗后若仍然存活，被攻击者获得经验（与攻击者相比较少）
        if self.exp >= self.nextExp:    # 经验满则升级
            self.levelUp()
        self.speed = randint(*SPIDER_ATTACKED_SPEED_RANGE)

    @staticmethod
    def nextLevel():    # 一个用于得到下一级的生成器
        level, maxHp, attack, nextExp = 0, 28, 3, 60
        # nextExp 升到下一级所需经验
        while True:
            if level < Spider.MaxLevel:
                level, maxHp, attack, nextExp = level + 1, maxHp + 2, attack + 1, 60
            else:
                maxHp, nextExp = maxHp + 1, 85
            yield level, maxHp, attack, nextExp

    def levelUp(self):
        self.exp -= self.nextExp            # 升级后将经验清除升级所需部分
        self.level, self.maxHp, self.attack, self.nextExp = next(self.levelIter)
        self.hp = self.maxHp                # 升级回满血
        if self.level < Spider.MaxLevel:
            x, y = self.image.get_size()    # 升一级图片放大一点
            self.image = pygame.transform.scale(self.image, (int(x * 1.2), int(y * 1.2)))
        print('%d号%s提升到了%d等级！' % (self.id, self.name, self.level))

    def draw(self, surface: pygame.Surface):
        super(Spider, self).draw(surface)
        if self.alive:
            # 画血条和经验条和等级
            x, y = self.location
            w, h = self.image.get_size()
            bar_x = x - w / 2
            bar_y = y + h / 2
            surface.fill((255, 0, 0), (bar_x, bar_y, self.maxHp, 3))
            surface.fill((0, 255, 0), (bar_x, bar_y, self.hp, 3))
            surface.fill((0, 255, 255), (bar_x, bar_y + 4, self.nextExp / 3, 3))
            surface.fill((0, 0, 255), (bar_x, bar_y + 4, self.exp / 3, 3))
            surface.blit(self.getFont().render('%d' % self.level, True, TEXT_COLOR),
                         (x + w / 2, y - h / 2, x + w / 2 + 12, y - h / 2 + 12))

    def step(self, timePassed):
        x, y = self.location
        if self.alive and x > SCREEN_SIZE[0] + 2 or y < -2:      # 设置为蜘蛛到达右边界或上边界即消失
            # 加上存活的条件是为了防止少数时候在即将离开画面之前死亡，从而导致remove一个空的东西的情况
            print('%d号%s离开了画面！' % (self.id, self.name))
            self.invalidate()
            return
        super(Spider, self).step(timePassed)


class Ant(WorldEntity):
    Image = None

    @staticmethod
    def loadImage():
        if Ant.Image is None:
            Ant.Image = pygame.image.load(getPath('resource', 'ant.jpg')).convert_alpha()
            Ant.Image = pygame.transform.scale(Ant.Image, (30, 20))
        return Ant.Image

    def __init__(self, world=None):
        super(Ant, self).__init__('ant', world)
        self.image = self.loadImage()
        self.alive = True
        self.levelIter = self.nextLevel()
        self.level, self.maxHp, self.attack, self.nextExp = next(self.levelIter)
        self.hp = self.maxHp
        self.speed = 30. + randint(-10, 10)
        self.exp = 0
        self.carryImage = None  # 蚂蚁携带的东西的图片

        self.brain.addState(AntExploring(self))
        self.brain.addState(AntSeeking(self))
        self.brain.addState(AntDelivering(self))
        self.brain.addState(AntHunting(self))

    def carry(self, image):
        self.carryImage = image

    def drop(self, surface):
        # drop the carry image onto surface (often background)
        if self.carryImage:
            x, y = self.location
            w, h = self.carryImage.get_size()
            surface.blit(self.carryImage, (x - w, y - h / 2))
            self.carryImage = None

    def draw(self, surface: pygame.Surface):
        super(Ant, self).draw(surface)
        if self.carryImage:
            x, y = self.location
            w, h = self.carryImage.get_size()
            surface.blit(self.carryImage, (x - w, y - h / 2))

    @staticmethod
    def nextLevel():
        level, maxHp, attack, nextExp = 0, 18, 1, 12
        while True:
            if level < Spider.MaxLevel:
                level, maxHp, attack, nextExp = level + 1, maxHp + 5, attack + 1, 12
            else:
                maxHp, nextExp = maxHp + 1, 32
            yield level, maxHp, attack, nextExp


def printWorld(world):
    for entity in world.entities.values():
        print(repr(entity), entity.valid)


def test():
    world = World()
    e1 = WorldEntity('ant', world)
    e2 = WorldEntity('spider', world)

    printWorld(world)

    e1.invalidate()

    printWorld(world)

    world.step(0)

    printWorld(world)

if __name__ == '__main__':
    test()
