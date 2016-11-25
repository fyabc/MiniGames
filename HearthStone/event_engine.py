#! /usr/bin/python
# -*- encoding: utf-8 -*-

from collections import deque, defaultdict


__author__ = 'fyabc'


class Event:
    CreatedEventNumber = 0

    def __init__(self):
        self.id = Event.CreatedEventNumber
        Event.CreatedEventNumber += 1

    def __str__(self):
        return '{}(id={})'.format(self.__class__.__name__, self.id)

    def __repr__(self):
        return self.__str__()

    def happen(self):
        pass


class Handler:
    CreatedHandlerNumber = 0

    # Event types for this class of handler to listen
    event_types = []

    def __init__(self):
        self.id = Handler.CreatedHandlerNumber
        Handler.CreatedHandlerNumber += 1

        # [NOTE] If a handler is not alive, it will not process any events,
        # and will be removed after a event was processed.
        # [NOTE] When a handler processes a event, it may disable other handlers
        # (e.g. kill a minion and invalidate all handlers it added.)
        # so the list of handlers will be changed in iteration.
        # so we set them into dead, then remove them after the iteration.
        self.alive = True

    def __str__(self):
        return '{}(id={}, alive={})'.format(self.__class__.__name__, self.id, self.alive)

    def __repr__(self):
        return self.__str__()

    def kill(self):
        self.alive = False

    def process(self, event):
        if self.alive:
            self._process(event)

    def _process(self, event):
        pass


class EventEngine:
    def __init__(self, event_types, maxsize=None):
        self.event_types = set(event_types)
        self.events = deque(maxlen=maxsize)

        # [NOTE] All handlers are divided by the event types they listen.
        # One handler may listen to more than one event type.
        # [NOTE] All handlers in this EventEngine which listen same event type
        # are sorted by the time they are added.
        self.handlers = defaultdict(list)

    def register_event_type(self, *event_types):
        self.event_types.update(event_types)

    def add_handler(self, handler):
        pass

    def remove_dead_handlers(self, event):
        for event_type in type(event).__mro__:
            self.handlers[event_type] = [handler for handler in self.handlers[event_type] if handler.alive]

    def dispatch_event(self, user_event):
        """dispatch a user event to handlers.
        [NOTE] user_event may cause several other events.

        :param user_event: the event given by user.
        :return: None
        """

        self.events.append(user_event)

        while self.events:
            event = self.events.popleft()
            event.happen()

            # [NOTE] When a event happens, the handler of this event type and it's base types
            # both need to be called.
            for event_type in type(event).__mro__:
                for handler in self.handlers[event_type]:
                    handler.process(event)

            # [NOTE] After iteration, remove all dead handlers related to this event.
            self.remove_dead_handlers(event)
