import random
from unittest.mock import MagicMock

from state.actor_decorator import ConfusedActorDecorator


def test_init():
    actor = MagicMock()
    decorator = ConfusedActorDecorator(actor)
    assert decorator.decorated_actor == actor


def test_get_icon_confused():
    actor = MagicMock()
    decorator = ConfusedActorDecorator(actor)
    assert decorator.get_icon() == "z"


def test_get_name():
    actor = MagicMock()
    actor.get_name.return_value = "Goblin"
    decorator = ConfusedActorDecorator(actor)
    assert decorator.get_name() == "Goblin"


def test_move_confused():
    actor = MagicMock()
    actor.coordinates = MagicMock()
    actor.coordinates.x = 1
    actor.coordinates.y = 2
    random.randint = MagicMock(return_value=1)
    decorator = ConfusedActorDecorator(actor)
    new_coordinates = decorator.update(None)
    assert abs(new_coordinates.x - actor.coordinates.x) <= 1
    assert abs(new_coordinates.y - actor.coordinates.y) <= 1
