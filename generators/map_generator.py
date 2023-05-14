import random
from typing import Set

import state.physical_object as po
from generators.enemy_generator import EnemyGenerator
from generators.item_generator import ItemGenerator
from state.enemy import Enemy, AggressiveEnemy
from state.item import Sword
from state.game_map import GameMap, Room
from state.physical_object_factory import get_physical_object


def generate_corridor(n: int) -> Room:
    first_room = Room("0")
    prev_direction = ""
    current_room = first_room
    directions = {"left", "right", "top", "bottom"}

    for i in range(1, n):
        new_room = Room(str(i))
        available_directions = directions - {prev_direction}
        direction = random.choice(list(available_directions))
        current_room.connect(new_room, direction)
        current_room = new_room
        prev_direction = Room.opposite_direction(direction)

    return first_room


def fill_room_from_file(room: Room, path: str):
    with open(path, "r") as levels_file:
        game_map = [list(line.strip()) for line in levels_file.readlines()]
        room.game_map = [[get_physical_object(c) for c in row] for row in game_map]
        room.height = len(game_map)
        room.width = len(game_map[0])


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

    @staticmethod
    def generate_new_map(level=1) -> GameMap:
        def dfs(room: Room, visited: Set[Room]):
            visited.add(room)
            next_rooms = [
                r for r in room.get_available_rooms().keys() if r not in visited
            ]
            if next_rooms:
                MapGenerator._fill_room(room, level)
                room.add_doors_to_room(po.Door())
                dfs(next_rooms[0], visited)
            else:
                MapGenerator._fill_final_room(room, level)

        number_of_rooms = MapGenerator._get_count_rooms(level)
        root = MapGenerator._generate_rooms(number_of_rooms)
        dfs(root, set())
        return GameMap(root, number_of_rooms)

    @staticmethod
    def _generate_rooms(number_rooms: int) -> Room:
        # return start room (root)
        return generate_corridor(number_rooms)

    @staticmethod
    def _get_count_rooms(level: int) -> int:
        # Power (Including Inverse and nth Root) using Curve Fitting
        # points:
        # (1, 5)  (2, 8)  (3, 10) (4, 11) (5, 13)
        # (6, 14) (7, 14) (8, 15) (9, 15) (10, 16)
        y = int(448.8 * (level**0.00102) - 443)
        rnd = random.randint(-1, 1)
        return y + rnd

    @staticmethod
    def _fill_room(room: Room, level=1):
        fill_room_from_file(room, f"levels/template.txt")
        room.enemies = EnemyGenerator.generate_enemies(level, room.game_map)
        ItemGenerator.generate_items(level, room.game_map)

    @staticmethod
    def _fill_final_room(room: Room, level=1):
        fill_room_from_file(room, f"levels/level_{level}.txt")
        room.enemies = {AggressiveEnemy(60, 17)}
        room.game_map[20][10] = Sword()
        room.is_finale = True
