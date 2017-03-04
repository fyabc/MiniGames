#! /usr/bin/python
# -*- coding: utf-8 -*-

import random

from ..utils.vector2 import Vector2

__author__ = 'fyabc'


class World:
    def __init__(self, size):
        self.entities = {}
        self.next_entity_id = 0
        self.size = size
        self.time = 0

    def add_entity(self, entity):
        self.entities[self.next_entity_id] = entity
        entity.id = self.next_entity_id

        if entity.world is None:
            entity.world = self
        entity.valid = True

        self.next_entity_id += 1

    def remove_entity(self, entity):
        del self.entities[entity.id]

    def get_entity(self, entity_id):
        return self.entities.get(entity_id, None)

    def step(self, time_passed):
        # You cannot delete an entity when iterating entities, so add its id into lostEntities,
        # then remove them after iteration.
        self.time += 1

        lost_entities = set()

        for entity in self.entities.values():
            if entity.valid:
                entity.step(time_passed)
            if not entity.valid:
                lost_entities.add(entity.id)

        # remove all invalid entities.
        self_entities = self.entities   # This is to speed up.
        for entity_id in lost_entities:
            del self_entities[entity_id]

    def get_close_entity(self, entity_type, location, see_range=100.0, get_all=False):
        location = Vector2(*location)

        result = []

        for entity in self.entities.values():
            if entity.valid and isinstance(entity, entity_type):
                distance = location.distance(entity.location)

                if distance < see_range:
                    if get_all:
                        result.append(entity)
                    else:
                        return entity

        if get_all:
            return result
        else:
            return None

    def random_location(self):
        x, y = self.size

        return Vector2(random.uniform(0, x), random.uniform(0, y))


class AntSpiderWorld(World):
    pass
