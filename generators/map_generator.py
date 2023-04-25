import random
from typing import List
from generators.enemy_generator import EnemyGenerator
import state.physical_object as po
from state.game_object import GameObject
from state.physical_object_factory import get_physical_object


# class GameMap:
#     def __init__(self, width=0, height=0):
#         self.width = width
#         self.height = height
#         self.map = None

# TODO: выбросить из map_generator
class Room:
    def __init__(self, name: str):
        # TODO: вынести в GameMap
        self.width = 0
        self.height = 0

        self.name = name
        self.type = None
        self.left = None
        self.right = None
        self.top = None
        self.bottom = None
        self.game_map : List[List[GameObject]] = []
        self.enemies = set()
        self.is_finale = False

    def connect(self, other, direction):
        if direction == 'left':
            self.left = other
            other.right = self
        elif direction == 'right':
            self.right = other
            other.left = self
        elif direction == 'top':
            self.top = other
            other.bottom = self
        elif direction == 'bottom':
            self.bottom = other
            other.top = self
        else:
            raise ValueError("Invalid direction")

    def __str__(self):
        return f"[ {self.name} ]"


def generate_corridor(n: int) -> Room:
    name_i = 0
    first_room = Room(str(name_i))
    current_room = first_room
    previous_direction = ""
    directions = {"left", "right", "top", "bottom"}
    for _ in range(n - 1):
        name_i += 1
        new_room = Room(str(name_i))
        directions.discard(previous_direction)
        available_directions = [d for d in directions]
        direction = random.choice(available_directions)
        if previous_direction:
            directions.add(previous_direction)
        if direction == "left":
            current_room.left = new_room
            new_room.right = current_room
            previous_direction = "right"
        elif direction == "right":
            current_room.right = new_room
            new_room.left = current_room
            previous_direction = "left"
        elif direction == "top":
            current_room.top = new_room
            new_room.bottom = current_room
            previous_direction = "bottom"
        elif direction == "bottom":
            current_room.bottom = new_room
            new_room.top = current_room
            previous_direction = "top"
        current_room = new_room

    return first_room


def fill_room_from_file(room: Room, path: str):
    height = 0
    width = 0
    with open(path, "r") as levels_file:
        i = 0
        j = 0
        game_map = room.game_map
        for line in levels_file.readlines():
            game_map.append([])
            for c in list(line.strip()):
                game_map[i].append(get_physical_object(c))
                j += 1
            width = j - 1
            i += 1
            j = 0
        height = i - 1
    room.height = height
    room.width = width


class MapGenerator:

    def __init__(self, level=1):
        self.level = level
        self.root = None
        self.number_rooms = 0

    def generate_new_map(self):
        def dfs(room: Room, vis: set):
            vis.add(room)
            next_room = [r for r in [room.left, room.right, room.top, room.bottom]
                         if r not in vis
                         and r is not None]
            if next_room:
                self.__fill_room(room)
                self.__add_doors_to_room(room)
                dfs(next_room[0], vis)
            else:
                self.__fill_final_room(room)

        self.__generate_rooms()
        visited = set()
        dfs(self.root, visited)

        return self.root

    def up_level(self):
        self.level += 1

    def __generate_rooms(self):
        self.number_rooms = self.__get_count_rooms()
        self.root = generate_corridor(self.number_rooms)

    def __get_count_rooms(self):
        # Power (Including Inverse and nth Root) using Curve Fitting
        # points:
        # (1, 5)  (2, 8)  (3, 10) (4, 11) (5, 13)
        # (6, 14) (7, 14) (8, 15) (9, 15) (10, 16)
        y = int(448.8 * (self.level ** 0.00102) - 443)
        rnd = random.randint(-1, 1)
        return y + rnd

    def __fill_room(self, room: Room):
        fill_room_from_file(room, f"levels/template.txt")
        for enemy in EnemyGenerator.generate_enemies(self.level, room.game_map):
            room.enemies.add(enemy)

    def __fill_final_room(self, room: Room):
        fill_room_from_file(room, f"levels/level_{self.level}.txt")
        room.is_finale = True

    def __add_doors_to_room(self, room: Room):
        width = room.width
        height = room.height
        game_map = room.game_map
        if room.top:
            game_map[1][width // 2] = po.Door()
            game_map[1][width // 2 + 1] = po.Door()
        if room.bottom:
            game_map[height - 1][width // 2] = po.Door()
            game_map[height - 1][width // 2 + 1] = po.Door()
        if room.left:
            game_map[height // 2][0] = po.Door()
            game_map[height // 2 + 1][0] = po.Door()
        if room.right:
            game_map[height // 2][width] = po.Door()
            game_map[height // 2 + 1][width] = po.Door()


# debug system
# def print_corridor(corridor: Room, length: int):
#     current_room = corridor
#     prev = None
#     corridor_str = ""
#
#     for _ in range(length):
#         next_room = None
#         direction_arrow = ""
#
#         if current_room.left and current_room.left != prev:
#             direction_arrow = "←"
#             next_room = current_room.left
#         elif current_room.top and current_room.top != prev:
#             direction_arrow = "↑"
#             next_room = current_room.top
#         elif current_room.right and current_room.right != prev:
#             direction_arrow = "→"
#             next_room = current_room.right
#         elif current_room.bottom and current_room.bottom != prev:
#             direction_arrow = "↓"
#             next_room = current_room.bottom
#
#         corridor_str += current_room.name + " " + direction_arrow + " "
#         prev = current_room
#         current_room = next_room
#
#     print(corridor_str.rstrip())
#
#
# print_corridor(generate_corridor(5), 5)
