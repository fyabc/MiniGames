#! /usr/bin/python
# -*- coding: utf-8 -*-


from HearthStone.event_engine import Event, Handler, EventEngine

__author__ = 'fyabc'


def _test():
    class UserEvent(Event):
        pass

    engine = EventEngine()

    handler = Handler()
    handler.event_types.append(Event)

    engine.add_handler(handler)

    engine.dispatch_event(UserEvent())

    print(UserEvent.get_ancestors())
    print(Event.get_ancestors())


if __name__ == '__main__':
    _test()
