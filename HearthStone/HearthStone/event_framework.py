#! /usr/bin/python
# -*- encoding: utf-8 -*-

from collections import deque, defaultdict

__author__ = 'fyabc'


class Event:
    CreatedEventNumber = 0

    def __init__(self):
        self.id = Event.CreatedEventNumber
        Event.CreatedEventNumber += 1

        # Handlers before the event may disable it. If an event is disabled, it will not happen.
        self.alive = True

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

    def disable(self):
        self.alive = False

    def happen(self):
        if self.alive:
            self._happen()

    def _happen(self):
        pass


class Handler:
    CreatedHandlerNumber = 0

    # Event types for this class of handler to listen
    # [WARNING] If one event type is another's super class, the event may be processed twice.
    # We need to avoid this.
    event_types = []

    # Decide if the handler process before or after the event happens.
    # [NOTE] True is before, False is after.
    BeforeOrAfter = False

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
        # [NOTE] All handlers are divided by the time of process (before or after the event happens)
        self.before_handler_set = defaultdict(list)
        self.after_handler_set = defaultdict(list)

    # Event type
    @property
    def event_types(self):
        return list(self.events.keys())

    def add_event_type(self, *event_types):
        for event_type in event_types:
            # [NOTE] The defaultdict will set the default value if not exists.
            _ = self.events[event_type]

    # Handler
    def _get_handler_set(self, before_or_after):
        if before_or_after:
            return self.before_handler_set
        return self.after_handler_set

    def add_handler(self, handler):
        """Add a handler into the engine.
        It will append it into all handler lists of event types in handler's event_types.
        It will create event type entry

        :param handler: the handler to be added
        :return: None
        """

        assert isinstance(handler, Handler)

        handler_set = self._get_handler_set(handler.BeforeOrAfter)

        for event_type in handler.event_types:
            handler_set[event_type].append(handler)

    def remove_handler(self, handler):
        """Remove the handler from the engine.
        It will remove it from all handler lists of event types in handler's event_types.

        :param handler: the handler to be removed
        :return: None
        """

        assert isinstance(handler, Handler)

        handler_set = self._get_handler_set(handler.BeforeOrAfter)

        for event_type in handler.event_types:
            handlers = handler_set.get(event_type, None)
            if handlers is not None:
                handlers.remove(handler)

    def remove_dead_handlers(self, event):
        for event_type in event.get_ancestors():
            if event_type in self.before_handler_set:
                self.before_handler_set[event_type] = [handler for handler in self.before_handler_set[event_type] if handler.alive]
            if event_type in self.after_handler_set:
                self.after_handler_set[event_type] = [handler for handler in self.after_handler_set[event_type] if handler.alive]

    # Event
    def add_event(self, event):
        self.events.append(event)

    def add_events(self, *events):
        self.events.extend(events)

    def dispatch_event(self, event):
        """Dispatch a user event to handlers.
        This method will clear the event queue.
        [NOTE] `event` may cause several other events.

        :param event: event given by user.
        :return: None
        """

        self.events.append(event)

        while self.events:
            event = self.events.popleft()

            # [NOTE] When a event happens, the handler of this event type and it's base types
            # both need to be called.
            for event_type in event.get_ancestors():
                handlers = self.before_handler_set.get(event_type, None)
                if handlers is not None:
                    for handler in handlers:
                        handler.process(event)

            event.happen()

            for event_type in event.get_ancestors():
                handlers = self.after_handler_set.get(event_type, None)
                if handlers is not None:
                    for handler in handlers:
                        handler.process(event)

            # [NOTE] After iteration, remove all dead handlers related to this event.
            self.remove_dead_handlers(event)