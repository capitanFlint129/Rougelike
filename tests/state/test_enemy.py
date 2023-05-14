import pytest
from unittest.mock import MagicMock

import state.physical_object as po
from state.hero import Hero
from state.actor import Actor
from state.item import Sword
from state.enemy import Enemy, CloneableEnemy
import state.enemy_state as es
from state.item import Item


class MockGameState:
    def __init__(self):
        self.game_map = None
        self.hero = None


@pytest.fixture
def game_state():
    return MockGameState()


def test_enemy_get_icon():
    enemy = Enemy()
    assert enemy.get_icon() == "*"


def test_enemy_get_name():
    enemy = Enemy()
    assert enemy.get_name() == "enemy"


def test_enemy_equip():
    enemy = Enemy()
    item = Item("test_item")
    enemy.equip(item)
    assert enemy.inventory == []


def test_enemy_get_damage():
    enemy = Enemy()
    enemy.health = 10
    enemy.get_damage(5)
    assert enemy.health == 5
    assert enemy.wounded == False


def test_enemy_get_damage_wounded():
    enemy = Enemy()
    enemy.movement.state = es.CowardlyEnemyState()
    enemy.health = 10
    enemy.get_damage(7)
    assert enemy.health == 3
    assert enemy.wounded == True
    assert type(enemy.original_state) == type(enemy.movement.state)


def test_enemy_get_item():
    enemy = Enemy()
    item = Item("test_item")
    enemy.get_item(item)
    assert enemy.inventory == []


def test_enemy_heal():
    enemy = Enemy()
    enemy.movement.state = es.AggressiveEnemyState()
    enemy.get_damage(9)
    assert enemy.wounded
    assert enemy.health == 1
    assert enemy.movement.state == enemy.wounded_state


def test_enemy_heal_not_wounded():
    enemy = Enemy()
    enemy.health = 10
    enemy.wounded = False
    enemy.regeneration = 1
    enemy._heal()
    assert enemy.health == 10
    assert enemy.movement.state == None


def test_enemy_creation():
    enemy = Enemy()
    assert isinstance(enemy, Actor)
    assert isinstance(enemy.movement, es.EnemyMovement)


def test_enemy_get_icon():
    enemy = Enemy()
    assert enemy.get_icon() == "*"


def test_enemy_get_name():
    enemy = Enemy()
    assert enemy.get_name() == "enemy"


def test_enemy_equip():
    enemy = Enemy()
    item = Sword()
    enemy.equip(item)
    assert enemy.get_item(item) is None


def test_enemy_get_item():
    enemy = Enemy()
    item = Sword()
    assert enemy.get_item(item) is None


def test_cloneable_enemy_creation():
    enemy = CloneableEnemy(1, 2)
    assert isinstance(enemy, Enemy)
    assert enemy.cloning_probability == 0.5


def test_cloneable_enemy_clone():
    enemy = CloneableEnemy(1, 2)
    clone = enemy.clone()
    assert isinstance(clone, CloneableEnemy)
    assert clone.coordinates == enemy.coordinates
    assert clone.cloning_probability == enemy.cloning_probability


def test_cloneable_enemy_update(game_state):
    enemy = CloneableEnemy(1, 2)
    enemy.cloning_probability = 1
    enemy.movement = MagicMock()
    game_state.hero = Hero(3, 4)
    game_state.game_map = MockMap()
    game_state.game_map.set_object_at(2, 2, Sword())
    game_state.game_map.set_object_at(2, 3, Sword())
    game_state.game_map.set_object_at(2, 4, Sword())
    game_state.game_map.set_object_at(3, 2, Sword())
    game_state.game_map.set_object_at(3, 4, Sword())
    game_state.game_map.set_object_at(4, 2, Sword())
    game_state.game_map.set_object_at(4, 3, Sword())
    game_state.game_map.set_object_at(4, 4, Sword())
    game_state.game_map.set_object_at(2, 5, enemy)
    enemy.update(game_state)
    assert len(game_state.game_map.get_enemies()) == 2  # One clone should be added


class MockMap:
    def __init__(self):
        self.map = {}

    def get_object_at(self, x, y):
        return self.map.get((x, y), po.FreeSpace())

    def set_object_at(self, x, y, obj):
        self.map[(x, y)] = obj

    def get_enemies(self):
        return set(filter(lambda x: isinstance(x, Enemy), self.map.values()))
