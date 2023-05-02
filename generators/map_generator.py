import random
from typing import List, Set
from generators.enemy_generator import EnemyGenerator
from generators.item_generator import ItemGenerator
import state.physical_object as po
from state.enemy import Enemy
from state.game_object import GameObject
from state.item import Sword
from state.physical_object_factory import get_physical_object


# TODO: Создать game_map.py, вынести руму туда
class Room:
    def __init__(self, name: str):
        self.width = 0
        self.height = 0
        self.name = name
        self.type = None
        self.left = None
        self.right = None
        self.top = None
        self.bottom = None
        self.game_map: List[List[GameObject]] = []
        self.enemies = set()
        self.is_finale = False

    def connect(self, other: "Room", direction: str):
        if direction == "left":
            self.left = other
            other.right = self
        elif direction == "right":
            self.right = other
            other.left = self
        elif direction == "top":
            self.top = other
            other.bottom = self
        elif direction == "bottom":
            self.bottom = other
            other.top = self
        else:
            raise ValueError("Invalid direction")

    def __str__(self):
        return f"[ {self.name} ]"


def generate_corridor(n: int) -> Room:
    first_room = Room("0")
    prev_direction = ""
    current_room = first_room
    opposite_direction = {
        "left": "right",
        "right": "left",
        "top": "bottom",
        "bottom": "top",
    }

    for i in range(1, n):
        new_room = Room(str(i))
        available_directions = set(opposite_direction.keys()) - {prev_direction}
        direction = random.choice(list(available_directions))
        current_room.connect(new_room, direction)
        current_room = new_room
        prev_direction = opposite_direction[direction]

    return first_room


def fill_room_from_file(room: Room, path: str):
    with open(path, "r") as levels_file:
        game_map = [list(line.strip()) for line in levels_file.readlines()]
        room.game_map = [[get_physical_object(c) for c in row] for row in game_map]
        room.height = len(game_map)
        room.width = len(game_map[0])


class MapGenerator:
    def __init__(self, level=1):
        self.level = level
        self.root = None
        self.number_rooms = 0

    def generate_new_map(self):
        def dfs(room: Room, visited: Set[Room]):
            visited.add(room)
            next_rooms = [
                r
                for r in [room.left, room.right, room.top, room.bottom]
                if r not in visited and r is not None
            ]
            if next_rooms:
                self._fill_room(room)
                self._add_doors_to_room(room)
                dfs(next_rooms[0], visited)
            else:
                self._fill_final_room(room)

        self._generate_rooms()
        dfs(self.root, set())

        return self.root

    def _generate_rooms(self):
        self.number_rooms = self._get_count_rooms()
        self.root = generate_corridor(self.number_rooms)

    def _get_count_rooms(self):
        # Power (Including Inverse and nth Root) using Curve Fitting
        # points:
        # (1, 5)  (2, 8)  (3, 10) (4, 11) (5, 13)
        # (6, 14) (7, 14) (8, 15) (9, 15) (10, 16)
        y = int(448.8 * (self.level**0.00102) - 443)
        rnd = random.randint(-1, 1)
        return y + rnd

    def _fill_room(self, room: Room):
        fill_room_from_file(room, f"levels/template.txt")
        room.enemies = EnemyGenerator.generate_enemies(self.level, room.game_map)
        ItemGenerator.generate_items(self.level, room.game_map)

    def _fill_final_room(self, room: Room):
        fill_room_from_file(room, f"levels/level_{self.level}.txt")
        room.enemies = {Enemy(60, 17)}
        room.game_map[20][10] = Sword()
        room.is_finale = True

    @staticmethod
    def _add_doors_to_room(room: Room):
        width = room.width
        height = room.height
        game_map = room.game_map
        if room.top:
            game_map[0][width // 2] = po.Door()
            game_map[0][width // 2 - 1] = po.Door()
        if room.bottom:
            game_map[height - 1][width // 2] = po.Door()
            game_map[height - 1][width // 2 - 1] = po.Door()
        if room.left:
            game_map[height // 2][0] = po.Door()
            game_map[height // 2 - 1][0] = po.Door()
        if room.right:
            game_map[height // 2][width - 1] = po.Door()
            game_map[height // 2 - 1][width - 1] = po.Door()
