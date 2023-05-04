from abc import ABC

import pytest
from state.actor import Actor
from utils.coordinates import Coordinates
from state.item import Item, Sword, Shield


class ActorForTests(Actor, ABC):
    def get_icon(self):
        return "@"

    def get_name(self):
        return "test"


def test_actor_initialization():
    actor = ActorForTests(1, 2)

    assert actor.inventory == set()
    assert actor.equipped == set()
    assert actor.health == 10
    assert actor.power == 1
    assert actor.is_alive is True
    assert actor.coordinates == Coordinates(1, 2)
    assert str(actor) == "@"


def test_actor_attack():
    actor1 = ActorForTests(1, 2)
    actor2 = ActorForTests(3, 4)

    actor1.attack(actor2)

    assert actor2.health == 9


def test_actor_get_item():
    actor = ActorForTests(1, 2)
    sword = Sword()

    actor.get_item(sword)

    assert sword in actor.inventory


def test_actor_equip_unequip():
    actor = ActorForTests(1, 2)
    sword = Sword()

    actor.get_item(sword)
    actor.equip(sword)

    assert sword in actor.equipped

    actor.unequip(sword)

    assert sword not in actor.equipped


def test_actor_get_damage():
    actor = ActorForTests(1, 2)
    shield = Shield()

    actor.get_item(shield)
    actor.equip(shield)

    actor.get_damage(5)

    assert actor.health == 10
    assert actor.is_alive is True

    actor.get_damage(20)

    assert actor.health == 0
    assert actor.is_alive is False


def test_actor_coordinates():
    actor = ActorForTests(1, 2)

    assert actor.get_x() == 1
    assert actor.get_y() == 2

    actor.set_x(3)
    actor.set_y(4)

    assert actor.get_x() == 3
    assert actor.get_y() == 4

    actor.move_to(5, 6)

    assert actor.get_x() == 5
    assert actor.get_y() == 6
