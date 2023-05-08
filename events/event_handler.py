import time
from typing import Set


class Event:
    def __init__(self, callback, args=None, delay=1, event_name=""):
        self.event_name = event_name
        self.callback = callback
        self.args = args or []
        self.execution_time = time.time() + delay

    def execute(self):
        self.callback(*self.args)


class EventHandler:
    _events: Set[Event] = set()

    @classmethod
    def add_event(cls, event):
        cls._events.add(event)

    @classmethod
    def remove_event(cls, event: Event):
        cls._events.discard(event)

    @classmethod
    def update(cls):
        current_time = time.time()
        events_to_remove = set()
        for event in cls._events:
            if current_time >= event.execution_time:
                event.execute()
                events_to_remove.add(event)
        cls._events -= events_to_remove

    @classmethod
    def clear_events(cls):
        cls._events = set()
