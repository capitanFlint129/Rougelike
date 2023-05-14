import pytest
from state.game_map import Room
from generators.map_builder import (
    RandomMapBuilder,
    FinalRoomBuilder,
    MapDirector,
)


class MockEnemyFactory:
    @staticmethod
    def create_enemies(level, game_map):
        return {"enemy1", "enemy2"}


class MockItemGenerator:
    @staticmethod
    def generate_items(level, game_map):
        game_map[0][0] = "sword"


class TestMapBuilder:
    @pytest.fixture
    def random_builder(self):
        return RandomMapBuilder()

    @pytest.fixture
    def final_builder(self):
        return FinalRoomBuilder()

    @pytest.fixture
    def map_director(self):
        return MapDirector()

    def test_random_map_builder(self, random_builder):
        random_builder.generate_map(10, 10)
        assert random_builder.room.width == 10
        assert random_builder.room.height == 10
        assert isinstance(random_builder.room.game_map[0][0], object)

    def test_final_room_builder(self, final_builder):
        final_builder.set_level(1)
        final_builder.generate_map()
        assert final_builder.room.is_finale
        assert final_builder.room.width > 0
        assert final_builder.room.height > 0
        assert isinstance(final_builder.room.game_map[0][0], object)
        assert isinstance(final_builder.room.enemies, object)
        assert isinstance(final_builder.room.game_map[20][10], object)

    def test_map_director_with_random_builder(self, map_director, random_builder):
        map_director.set_builder(random_builder)
        map_director.set_enemy_factory(MockEnemyFactory())
        map_director.set_item_generator(MockItemGenerator())

        room = map_director.build_room(10, 10)
        assert isinstance(room, Room)
        assert room.width == 10
        assert room.height == 10
        assert room.game_map[0][0] == "sword"
        assert len(room.enemies) == 2

    def test_map_director_with_final_builder(self, map_director, final_builder):
        map_director.set_builder(final_builder)
        map_director.set_enemy_factory(MockEnemyFactory())
        map_director.set_item_generator(MockItemGenerator())

        room = map_director.build_room()
        assert isinstance(room, Room)
        assert room.is_finale
        assert room.width > 0
        assert room.height > 0
        assert isinstance(room.enemies.pop(), object)
