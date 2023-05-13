import pytest

from state.game_map import GameMap, Room
from generators.map_generator import MapGenerator


@pytest.fixture
def map_generator():
    return MapGenerator()


def test_generate_new_map_returns_instance_of_game_map(map_generator):
    game_map = map_generator.generate_new_map()
    assert isinstance(game_map, GameMap)


def test_generate_new_map_creates_map_with_at_least_one_room(map_generator):
    game_map = map_generator.generate_new_map()
    assert game_map.current_room is not None


def test_get_count_rooms_returns_an_integer(map_generator):
    count = map_generator._get_count_rooms(1)
    assert isinstance(count, int)


def test_generate_room_returns_instance_of_room(map_generator):
    room = map_generator._generate_room()
    assert isinstance(room, Room)


def test_generate_final_room_returns_instance_of_room(map_generator):
    final_room = map_generator._generate_final_room()
    assert isinstance(final_room, Room)
