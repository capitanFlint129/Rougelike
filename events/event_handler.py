import time
from typing import Set


class Event:
    """
    An object that represents an event in the game. An event consists of a callback function, a set of arguments for the
    function, a delay before the function is executed, and an optional name for the event. An Event object can be executed
    by calling its execute() method.
    """

    def __init__(self, callback, args=None, delay=1, event_name=""):
        """
        Initialize a new Event object.

        :param callback: The function to be executed when the event is triggered.
        :param args: A list of arguments to be passed to the function.
        :param delay: The number of seconds to wait before the event is triggered.
        :param event_name: An optional name for the event.
        """
        self.event_name = event_name
        self.callback = callback
        self.args = args or []
        self.execution_time = time.time() + delay

    def execute(self):
        """
        Execute the callback function with the given arguments.
        """
        self.callback(*self.args)


class EventHandler:
    """
    A class that manages events in the game. Events are stored in a set and can be added, removed, and updated by calling
    the corresponding methods.
    """

    _events: Set[Event] = set()

    @classmethod
    def add_event(cls, event):
        """
        Add an event to the set of events to be processed.

        :param event: The event to be added.
        """
        cls._events.add(event)

    @classmethod
    def remove_event(cls, event: Event):
        """
        Remove an event from the set of events to be processed.

        :param event: The event to be removed.
        """
        cls._events.discard(event)

    @classmethod
    def update(cls):
        """
        Update the set of events, executing any events whose execution time has been reached and removing them from the set.
        """
        current_time = time.time()
        events_to_remove = set()
        for event in cls._events:
            if current_time >= event.execution_time:
                event.execute()
                events_to_remove.add(event)
        cls._events -= events_to_remove

    @classmethod
    def clear_events(cls):
        """
        Remove all events from the set of events to be processed.
        """
        cls._events = set()
