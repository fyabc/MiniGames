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
        return '{}#{}'.format(self.__class__.__name__, self.id)

    def __repr__(self):
        return self.__str__()

    @classmethod
    def get_ancestors(cls):
        if '_ancestors' not in cls.__dict__:
            # [:-1] means remove the base class "object"
            setattr(cls, '_ancestors', cls.__mro__[:-1])
        return getattr(cls, '_ancestors')

    def happen(self):
        pass


class Handler:
    CreatedHandlerNumber = 0

    # Event types for this class of handler to listen
    # [WARNING] If one event type is another's super class, the event may be processed twice.
    # We need to avoid this.
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
        return '{}#{}(alive={})'.format(self.__class__.__name__, self.id, self.alive)

    def __repr__(self):
        return self.__str__()

    def kill(self):
        """kill the handler.
        [NOTE]: This method just set the alive bit to False, do not destroy it.
        It will be removed by the event engine soon.
        """

        self.alive = False

    def process(self, event):
        if self.alive:
            self._process(event)

    def _process(self, event):
        pass


class EventEngine:
    def __init__(self, maxsize=None, **kwargs):
        self.events = deque(maxlen=maxsize)

        event_types = kwargs.pop('event_types', [])
        self.add_event_type(*event_types)

        # [NOTE] All handlers are divided by the event types they listen.
        # One handler may listen to more than one event type.
        # [NOTE] All handlers in this EventEngine which listen same event type
        # are sorted by the time they are added.
        self.handlers = defaultdict(list)

    # Event type
    @property
    def event_types(self):
        return list(self.events.keys())

    def add_event_type(self, *event_types):
        for event_type in event_types:
            # [NOTE] The defaultdict will set the default value if not exists.
            _ = self.events[event_type]

    # Handler
    def add_handler(self, handler):
        """Add a handler into the engine.
        It will append it into all handler lists of event types in handler's event_types.
        It will create event type entry

        :param handler: the handler to be added
        :return: None
        """

        for event_type in handler.event_types:
            self.handlers[event_type].append(handler)

    def remove_handler(self, handler):
        """Remove the handler from the engine.
        It will remove it from all handler lists of event types in handler's event_types.

        :param handler: the handler to be removed
        :return: None
        """

        for event_type in handler.event_types:
            handlers = self.handlers.get(event_type, None)
            if handlers is not None:
                handlers.remove(handler)

    def remove_dead_handlers(self, event):
        for event_type in event.get_ancestors():
            if event_type in self.handlers:
                self.handlers[event_type] = [handler for handler in self.handlers[event_type] if handler.alive]

    # Event
    def add_events(self, *events):
        self.events.extend(events)

    def dispatch_event(self, *user_events):
        """Dispatch a user event to handlers.
        This method will clear the event queue.
        [NOTE] user_event may cause several other events.

        :param user_events: events given by user.
        :return: None
        """

        self.events.extend(user_events)

        while self.events:
            event = self.events.popleft()
            event.happen()

            # [NOTE] When a event happens, the handler of this event type and it's base types
            # both need to be called.
            for event_type in event.get_ancestors():
                handlers = self.handlers.get(event_type, None)
                if handlers is not None:
                    for handler in handlers:
                        handler.process(event)

            # [NOTE] After iteration, remove all dead handlers related to this event.
            self.remove_dead_handlers(event)
