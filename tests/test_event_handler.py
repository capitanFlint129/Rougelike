import time
from unittest.mock import MagicMock

from events.event_handler import Event, EventHandler


def test_event_execute():
    callback = MagicMock()
    event = Event(callback, [1, 2, 3], delay=0)
    event.execute()
    callback.assert_called_once_with(1, 2, 3)


def test_event_handler_add_event():
    event = Event(lambda: None, delay=0)
    EventHandler.add_event(event)
    assert event in EventHandler._events


def test_event_handler_remove_event():
    event = Event(lambda: None, delay=0)
    EventHandler._events.add(event)
    EventHandler.remove_event(event)
    assert event not in EventHandler._events


def test_event_handler_update():
    event1 = Event(MagicMock(), delay=1)
    event2 = Event(MagicMock(), delay=2)
    EventHandler._events = {event1, event2}
    time.sleep(1.5)
    EventHandler.update()
    event1.callback.assert_called_once()
    event2.callback.assert_not_called()
    assert event1 not in EventHandler._events
    assert event2 in EventHandler._events


def test_event_handler_clear_events():
    EventHandler._events = {Event(lambda: None, delay=0)}
    EventHandler.clear_events()
    assert EventHandler._events == set()
