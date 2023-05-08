import random

from state.game_map import GameMap, Room
from generators.map_builder import MapDirector, RandomMapBuilder, FinalRoomBuilder
from generators.enemies_factory import SciFiEnemyFactory, FantasyEnemyFactory
from state.physical_object import Door


class MapGenerator:
    """
    The MapGenerator class generates a GameMap with specific levels, where the map is a corridor with rooms,
    each with two exits. The method generate_new_map takes an optional level parameter and returns a new GameMap object.
    The method first generates a root room, and then performs a depth-first search to connect it to the other rooms,
    using the _fill_room method to populate each room with enemies and items.
    The last room in the map is generated with the _fill_final_room method and is marked as the finale.
    The number of rooms generated is based on a curve-fitting formula, which takes the level as input and returns
    a random number of rooms.
    """
    _director: MapDirector = MapDirector()

    @classmethod
    def generate_new_map(cls, level=1) -> GameMap:
        first_room = cls._generate_room(level)
        prev_direction = ""
        current_room = first_room
        directions = {"left", "right", "top", "bottom"}
        n = cls._get_count_rooms(level)

        for i in range(1, n):
            new_room = cls._generate_room(level) if i < n - 1 else cls._generate_final_room(level)
            available_directions = directions - {prev_direction}
            direction = random.choice(list(available_directions))
            current_room.connect(new_room, direction)
            current_room.add_doors_to_room(Door())
            current_room = new_room
            prev_direction = Room.opposite_direction(direction)

        return GameMap(first_room, n)

    @classmethod
    def _get_count_rooms(cls, level: int) -> int:
        # Power (Including Inverse and nth Root) using Curve Fitting
        # points:
        # (1, 5)  (2, 8)  (3, 10) (4, 11) (5, 13)
        # (6, 14) (7, 14) (8, 15) (9, 15) (10, 16)
        y = int(448.8 * (level ** 0.0102425) - 443)
        rnd = random.randint(-1, 1)
        return y + rnd

    @classmethod
    def _generate_room(cls, level=1) -> Room:
        cls._director.set_builder(RandomMapBuilder(level))
        width, height = random.randint(25, 50), random.randint(13, 23)
        cls._director.set_enemy_factory(
            SciFiEnemyFactory() if random.randint(0, 1) == 0 else FantasyEnemyFactory()
        )
        return cls._director.build_room(width, height)

    @classmethod
    def _generate_final_room(cls, level=1) -> Room:
        cls._director.set_builder(FinalRoomBuilder(level))
        return cls._director.build_room()
