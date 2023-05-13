import random
from unittest.mock import MagicMock
from generators.map_generator import (
    EnemyGenerator,
    ItemGenerator,
    generate_corridor,
    fill_room_from_file,
)
from state.game_map import GameMap, Room
from state.item import Sword, Shield
import state.physical_object as po


def test_generate_corridor():
    random.randint = MagicMock(return_value=1)
    first_room = generate_corridor(3)
    assert isinstance(first_room, Room)
    assert len(first_room.connections) == 4
    assert len(first_room.get_available_rooms()) == 1


def test_fill_room_from_file():
    room = Room("0")
    fill_room_from_file(room, "./levels/test_level.txt")
    assert room.width > 0
    assert room.height > 0
    game_map = room.game_map
    expected_objects = [
        po.Wall,
        po.FreeSpace,
        po.MapBorder,
        po.Coin,
        po.Thorn,
        po.Thorn,
        po.Thorn,
        po.Thorn,
        po.ExitPortal,
        po.Wall,
    ]
    for i, expected_object in enumerate(expected_objects):
        assert isinstance(game_map[0][i], expected_object)


def test_enemy_generator_generate_enemies():
    random.randint = MagicMock(return_value=2)
    enemies = EnemyGenerator.generate_enemies(level=1, map_array=[[0] * 10] * 10)
    assert len(enemies) == 1
    enemy = next(iter(enemies))
    assert enemy.get_x() == 2
    assert enemy.get_y() == 2


def test_item_generator_generate_items():
    random.randint = MagicMock(side_effect=[5, 0, 0, 6, 0, 1])
    map_array = [[None] * 10 for _ in range(10)]
    ItemGenerator.generate_items(level=1, map_array=map_array)
    assert isinstance(map_array[0][5], Sword)
    ItemGenerator.generate_items(level=1, map_array=map_array)
    assert isinstance(map_array[0][6], Shield)
