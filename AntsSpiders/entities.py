# -*- coding: utf-8 -*-

__author__ = 'fyabc'

import pygame

from Utils.vector2 import Vector2
from StateMachine.simpleBrain import Brain
from AntsSpiders.config import BG_COLOR
from AntsSpiders.states import AntExploring


class World:
    def __init__(self):
        self.entities = {}
        self.nextEntityID = 0

    def addEntity(self, newEntity):
        self.entities[self.nextEntityID] = newEntity
        newEntity.id = self.nextEntityID
        newEntity.world = self
        self.nextEntityID += 1

    def removeEntity(self, entity):
        self.entities[entity.id].world = None
        del self.entities[entity.id]

    def getEntity(self, entityID):
        if entityID in self.entities:
            return self.entities[entityID]
        else:
            return None

    def draw(self, surface: pygame.Surface):
        surface.fill(BG_COLOR)
        for entity in self.entities.values():
            entity.draw(surface)

    def step(self, timePassed):
        for entity in set(self.entities.values()):
            entity.step(timePassed)

    def getCloseEntity(self, name, location, seeRange=100.):
        locationVec = Vector2(*location)
        for entity in self.entities.values():
            if entity.name == name:
                distance = locationVec.distance(entity.location)
                if distance < seeRange:
                    return entity
        return None


class WorldEntity:
    def __init__(self, name, world):
        self.name = name
        self.world = world
        self.id = None
        world.addEntity(self)

        self.location = Vector2()
        self.destination = Vector2()
        self.speed = 0.

        self.brain = Brain()
        self.image = None

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
