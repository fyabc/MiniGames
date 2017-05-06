#! /usr/bin/python
# -*- encoding: utf-8 -*-

"""A simple event framework.

This framework implements an event engine.

Here are the elements of the engine:

    1. Event
        See docstring of `Event`.

    2. Handler
        See docstring of `Handler`.

    3. EventEngine
        See docstring of `EventEngine`.

"""

from collections import deque, defaultdict
from warnings import warn

__author__ = 'fyabc'


class Event:
    """The basic event class of the engine.

    Events are in a single-root class hierarchy.
        All events should be a instance of `Event`.

        Some properties of event:
            id: A unique id of the event.
                Created when the event was created, the early created event has smaller id.
            alive: Indicate if the event is alive.
                If a event is not alive (dead), it will not be processed by any handlers,
                and it will not happen (if not happened).

    Subclass of `Event` should override the method `_happen` (NOT `happen`).
    """

    CreatedEventNumber = 0

    def __init__(self):
        self.id = Event.CreatedEventNumber
        Event.CreatedEventNumber += 1

        # Handlers before the event may disable it. If an event is disabled, it will not happen,
        # and other handlers will not process it.
        self.alive = True

    def __str__(self):
        return '{}#{}'.format(self.__class__.__name__, self.id)

    def __repr__(self):
        return self.__str__()

    @classmethod
    def get_ancestors(cls):
        """Get the ancestor list of this event class.

        It is a lazy evaluated property.

        :return: The ancestor list, from the class of self to `Event`.
        """

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
    """The basic handler class of the engine.

    Handlers are in a single-root class hierarchy.
        All handlers should be a instance of `Handler`.

        Some properties of handler:
            id: A unique id of the handler.
                Created when the handler was created, the early created handler has smaller id.
            alive: Indicate if the handler is alive.
                If a handler is not alive (dead), it will not process any event,
                and it will be automatically removed by the engine soon
                (after the process of an event in this handler's event_types).
            event_types: (class variable) event types that the handler will process.
                When a event pushed into the engine, the handler will process this event if the type of the event:
                    Is in `event_types` of the handler, or
                    is a superclass of any event type in `event_types`.
                [WARNING]: if there are two types E1 and E2 in `event_types` that E1 is subclass of E2,
                    Then the event of E2 may be processed twice. So do NOT set event_types like this.
            BeforeOrAfter: (class variable) the handler will process the event before or after the event happens.
                True is before, False is after.

        [NOTE]: A handler may disable the event it processed, the event may also disable itself.
            If so, other handlers after this handler or event will not process it.

    Subclass of `Handler` should override the method `_process` (NOT `process`).
    """

    CreatedHandlerNumber = 0

    # Event types for this class of handler to listen
    # [WARNING] If one event type is another's super class, the event may be processed twice.
    # We need to avoid this.
    event_types = []

    # Decide if the handler process before or after the event happens.
    # [NOTE] True is before, False is after. Default to before.
    BeforeOrAfter = False

    def __init__(self):
        self.id = Handler.CreatedHandlerNumber
        Handler.CreatedHandlerNumber += 1

        # [NOTE] If a handler is not alive, it will not process any events,
        # and will be removed after a event was processed.
        # [NOTE] When a handler processes a event, it may disable other handlers
        # (e.g. kill a minion will invalidate all handlers it added.)
        # so the list of handlers will be changed in iteration.
        # so we set them into dead, then remove them after the iteration.
        self.alive = True

    def __str__(self):
        return '{}#{}(alive={})'.format(self.__class__.__name__, self.id, self.alive)

    def __repr__(self):
        return self.__str__()

    def disable(self):
        """disable the handler.
        [NOTE]: This method just set the alive flag to False, do not destroy it.
        It will be automatically removed by the event engine soon.
        """

        self.alive = False

    def process(self, event):
        if self.alive and event.alive:
            self._process(event)

    def _process(self, event):
        pass


class EventEngine:
    """The event engine class.

    The event dispatch procedure:
        See docstring of `dispatch_event`.
    """

    def __init__(self, maxsize=None, **kwargs):
        self._running = True

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

        # Event types that will terminate the engine.
        self.terminate_event_types = set()

        # The buffer for insert events (usually events created by other events or handlers)
        self.insert_event_buffer = deque()

        # Logging （for debug)
        logging_filename = kwargs.pop('logging_filename', None)

        if logging_filename is not None:
            try:
                self.logging_file = open(logging_filename, 'w', encoding='utf-8')
            except FileNotFoundError:
                self.logging_file = None
                warn('Cannot create the logging file.')
        else:
            self.logging_file = None

    # General methods
    def clear(self):
        """Clear events and handlers."""

        self.events.clear()
        self.before_handler_set.clear()
        self.after_handler_set.clear()

    def start(self, clear_handlers=False):
        self._running = True

        if clear_handlers:
            self.clear()
        else:
            self.events.clear()

    @property
    def running(self):
        return self._running

    # Event type
    @property
    def event_types(self):
        return list(self.events.keys())

    def add_event_type(self, *event_types):
        """Register event types into the engine."""

        for event_type in event_types:
            # [NOTE] The defaultdict will set the default value if not exists.
            _ = self.events[event_type]

    def add_terminate_event_type(self, event_type):
        self.terminate_event_types.add(event_type)

    # Handler
    def _get_handler_set(self, before_or_after):
        if before_or_after:
            return self.before_handler_set
        return self.after_handler_set

    def add_handler(self, handler):
        """Add a handler into the engine.
        It will append it into all handler lists of event types in handler's event_types.
        It will create event type entry if not exist.

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

    def _remove_dead_handlers(self, event):
        """Called by dispatch_events to remove dead handlers after one event is processed."""

        for event_type in event.get_ancestors():
            if event_type in self.before_handler_set:
                self.before_handler_set[event_type] = [
                    handler for handler in self.before_handler_set[event_type] if handler.alive]
            if event_type in self.after_handler_set:
                self.after_handler_set[event_type] = [
                    handler for handler in self.after_handler_set[event_type] if handler.alive]

    # Event
    def add_event(self, event):
        self.events.append(event)

    def add_events(self, *events):
        self.events.extend(events)

    def prepend_event(self, event):
        self.events.appendleft(event)

    def prepend_events(self, *events):
        self.events.extendleft(events)

    def insert_event(self, event):
        self.insert_event_buffer.append(event)

    # Run
    def dispatch_event(self, event=None):
        """Dispatch a user event to handlers.

        The event dispatch procedure:
            1. append the new event to the tail of event queue.
            2. repeat while the event queue is not empty:
                1) pop out the head of event queue -> `event`.
                2) get the ancestors of `event`.
                3) for the event type in ancestors, handlers (before) that registered to this event type process it.
                4) `event` happen (if `event` is alive)
                5) for the event type in ancestors, handlers (after) that registered to this event type process it.
                6) remove all dead handlers.
                7) if `event` is a terminate event, break, clear and return `event`; else continue.

        This method will clear the event queue.
        [NOTE] `event` may cause several other events, these event will be pushed back to the event queue.

        :param event: event given by user.
            If event is None, not any new event will be appended.
        :return: terminate event or None.
        """

        if not self._running:
            print('Error: The engine is not running, please call "start" method.')
            return

        if event is not None:
            self.events.append(event)

        terminate_event = None

        while self.events or self.insert_event_buffer:
            # Prepend all insert events.
            self.events.extendleft(self.insert_event_buffer)
            self.insert_event_buffer.clear()

            event = self.events.popleft()

            # [NOTE] When a event happens, the handler of this event type and it's base types
            # both need to be called.
            for event_type in event.get_ancestors():
                handlers = self.before_handler_set.get(event_type, None)
                if handlers is not None:
                    for handler in handlers:
                        handler.process(event)

            event.happen()

            if event.alive:
                for event_type in event.get_ancestors():
                    handlers = self.after_handler_set.get(event_type, None)
                    if handlers is not None:
                        for handler in handlers:
                            handler.process(event)

            self._logging_event(event)

            # [NOTE] After iteration, remove all dead handlers related to this event.
            self._remove_dead_handlers(event)

            if type(event) in self.terminate_event_types:
                terminate_event = event
                self._running = False
                self.events.clear()

                break

        # todo: run cartoon after all events?

        return terminate_event

    # Inner helper methods
    def _logging_event(self, event):
        if self.logging_file is not None:
            self.logging_file.write('{}{}\n'.format(event, '' if event.alive else '(X)'))
            self.logging_file.flush()
