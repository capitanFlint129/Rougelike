import pytest
from unittest.mock import MagicMock

from state.actor import Actor
from state.actor_decorator import ActorDecorator, ConfusedActorDecorator
from state.enemy import Enemy


def test_init():
    actor = MagicMock()
    decorator = ConfusedActorDecorator(actor)
    assert decorator.decorated_actor == actor


def test_get_icon():
    actor = MagicMock()
    actor.get_icon.return_value = "A"
    decorator = ConfusedActorDecorator(actor)
    assert decorator.get_icon() == "A"


def test_move():
    actor = MagicMock()
    actor.move.return_value = (1, 2)
    decorator = ConfusedActorDecorator(actor)
    assert decorator.move(None) == (1, 2)


def test_get_icon():
    actor = MagicMock()
    decorator = ConfusedActorDecorator(actor)
    assert decorator.get_icon() == "z"


def test_get_name():
    actor = MagicMock()
    actor.get_name.return_value = "Goblin"
    decorator = ConfusedActorDecorator(actor)
    assert decorator.get_name() == "Goblin"


def test_move():
    actor = MagicMock()
    actor.coordinates = MagicMock()
    actor.coordinates.x = 1
    actor.coordinates.y = 2
    decorator = ConfusedActorDecorator(actor)
    new_coordinates = decorator.move(None)
    assert abs(new_coordinates.x - actor.coordinates.x) <= 1
    assert abs(new_coordinates.y - actor.coordinates.y) <= 1
