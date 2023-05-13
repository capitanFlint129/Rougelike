# import pytest
# from state.game_map import GameMap, Room
# from generators.map_builder import RandomMapBuilder, FinalRoomBuilder, MapDirector
# from generators.enemies_factory import SciFiEnemyFactory, FantasyEnemyFactory
# from state.physical_object import Door
# from generators.map_generator import MapGenerator
#
#
# @pytest.fixture
# def mock_game_map(monkeypatch):
#     class MockRoom:
#         def __init__(self, doors=None):
#             self.doors = doors or {}
#
#         def add_doors_to_room(self, door):
#             pass
#
#         def connect(self, room, direction):
#             self.doors[direction] = room
#
#     monkeypatch.setattr("state.game_map.Room", MockRoom)
#
#     return GameMap(MockRoom(), 1)
#
#
# def test_generate_new_map_generates_map(mock_game_map):
#     level = 1
#     game_map = MapGenerator.generate_new_map(level)
#
#     assert isinstance(game_map, GameMap)
#
#
# def test_generate_new_map_has_correct_number_of_rooms(mock_game_map):
#     level = 1
#     game_map = MapGenerator.generate_new_map(level)
#
#     assert len(game_map.rooms) == MapGenerator._get_count_rooms(level)
#
#
# def test_get_count_rooms_returns_expected_values():
#     levels = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
#     expected_room_counts = [5, 8, 10, 11, 13, 14, 14, 15, 15, 16]
#
#     for level, expected_count in zip(levels, expected_room_counts):
#         room_count = MapGenerator._get_count_rooms(level)
#         assert (
#             room_count == expected_count
#             or room_count == expected_count + 1
#             or room_count == expected_count - 1
#         )
#
#
# def test_generate_room_returns_room_with_correct_dimensions():
#     level = 1
#     room = MapGenerator._generate_room(level)
#
#     assert 25 <= room.width <= 50
#     assert 13 <= room.height <= 23
#
#
# def test_generate_room_sets_enemy_factory_correctly():
#     level = 1
#     enemy_factories = [SciFiEnemyFactory, FantasyEnemyFactory]
#
#     for i in range(10):
#         room = MapGenerator._generate_room(level)
#         enemy_factory = MapGenerator._director.builder.enemy_factory
#
#         assert isinstance(enemy_factory, SciFiEnemyFactory) or isinstance(
#             enemy_factory, FantasyEnemyFactory
#         )
#
#
# def test_generate_final_room_sets_builder_correctly():
#     level = 1
#     final_room = MapGenerator._generate_final_room(level)
#
#     assert isinstance(MapGenerator._director.builder, FinalRoomBuilder)
#
#
# def test_generate_new_map_connects_rooms_with_doors(mock_game_map):
#     level = 1
#     game_map = MapGenerator.generate_new_map(level)
#
#     for room in game_map.rooms:
#         for direction, neighbor in room.doors.items():
#             assert direction in neighbor.doors
#             assert isinstance(room.doors[direction], Door)
#             assert isinstance(neighbor.doors[Room.opposite_direction(direction)], Door)
