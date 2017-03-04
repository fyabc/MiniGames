#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'fyabc'


class WorldEntity:
    def __init__(self, world=None, **kwargs):
        self.world = world

        self.id = None

        if world is not None:
            world.add_entity(self)

        self.valid = True

        init_loc = kwargs.pop('init_loc', None)
        self.location = world.random_location() if init_loc is None else init_loc

        init_dest = kwargs.pop('init_dest', None)
        self.dest = world.random_location() if init_dest is None else init_dest

        self.speed = kwargs.pop('speed', 0.0)

    def invalid(self):
        self.valid = False

    def step(self, time_passed):
        raise NotImplementedError()


class AIEntity(WorldEntity):
    """Entity controlled by AI. Contains a simple brain."""

    def __init__(self, world=None, **kwargs):
        super().__init__(world, **kwargs)

        self.brain = None

    def step(self, time_passed):
        pass


class UserEntity(WorldEntity):
    """Entity controlled by user."""

    def step(self, time_passed):
        pass
