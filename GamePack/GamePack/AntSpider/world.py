#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'fyabc'


class WorldEntity:
    def __init__(self, name, world=None):
        self.name = name
        self.world = world

        self.id = None

        if world is not None:
            world.add_entity(self)

        self.valid = True


class World:
    def __init__(self):
        self.entities = {}
        self.next_entity_id = 0

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


class AntSpiderWorld(World):
    pass
