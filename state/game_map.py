from state.enemy import Enemy
from state.game_object import GameObject

from typing import List, Set, Optional, Dict


class Room:
    """
    The game in question is presented in the form of a map consisting of connected rooms,
    each of which is randomly generated except for the final room.
    Each room is independent of the others and contains its own enemies and objects.
    The state of the game is saved as the player progresses through the rooms.

    This class represents a single room within the game. It includes instance variables for the room's map, enemies,
    and items (inside map). The room can be connected to neighboring rooms,
    and has a method for retrieving a dictionary of available rooms according to their direction.
    """

    def __init__(self, name: str):
        self.width = 0
        self.height = 0
        self.name = name
        self.type = None
        self.connections = {"left": None, "right": None, "top": None, "bottom": None}
        self.game_map: List[List[GameObject]] = []
        self.enemies: Set[Enemy] = set()
        self.is_finale = False

    def connect(self, other: "Room", direction: str):
        if direction in self.connections:
            self.connections[direction] = other
            other.connections[self.opposite_direction(direction)] = self
        else:
            raise ValueError("Invalid direction")

    @staticmethod
    def opposite_direction(direction: str) -> str:
        opposites = {"left": "right", "right": "left", "top": "bottom", "bottom": "top"}
        return opposites.get(direction, "")

    def __str__(self):
        return f"[{self.name}]"

    def get_available_rooms(self) -> Dict:
        available_rooms = dict()
        for d, r in self.connections.items():
            if r is not None:
                available_rooms[r] = d
        return available_rooms

    def add_doors_to_room(self, door: GameObject):
        """
        The "add_doors_to_room" method is used to add doors to a room in the game map.
        Initially, the game map does not contain doors, so this method is required to add the necessary doors
        that will lead the player to the next room.

        Args:
            door: GameObject that represents door

        Return:
            None
        """
        door_coordinates = {
            "top": [(0, self.width // 2), (0, self.width // 2 - 1)],
            "bottom": [
                (self.height - 1, self.width // 2),
                (self.height - 1, self.width // 2 - 1),
            ],
            "left": [(self.height // 2, 0), (self.height // 2 - 1, 0)],
            "right": [
                (self.height // 2, self.width - 1),
                (self.height // 2 - 1, self.width - 1),
            ],
        }

        for r, d in self.get_available_rooms().items():
            for y, x in door_coordinates[d]:
                self.game_map[y][x] = door


class GameMap:
    """
    Represents the game map as a collection of connected rooms.
    Responsible for providing data about the current game map, as well as for managing the change of the current room
    """

    def __init__(self, starting_room: Room, num_rooms: int):
        self.current_room: Room = starting_room
        self.number_of_rooms = num_rooms

    def change_room(self, direction: str) -> Optional[str]:
        if direction not in self.current_room.connections.keys():
            return f"Cannot move in the {direction} direction."
        next_room = self.current_room.connections[direction]
        if next_room:
            self.current_room = next_room
            return None
        else:
            return f"Cannot move in the {direction} direction."

    def add_room_to_current_room(self, room: Room, direction: str) -> None:
        self.current_room.connect(room, direction)

    def get_enemies(self) -> Set[Enemy]:
        return self.current_room.enemies

    def get_map(self) -> List[List[GameObject]]:
        return self.current_room.game_map

    def get_object_at(self, x: int, y: int) -> Optional[GameObject]:
        if 0 <= x < self.current_room.width and 0 <= y < self.current_room.height:
            return self.current_room.game_map[y][x]
        else:
            return None

    def set_object_at(self, x: int, y: int, game_object: GameObject) -> None:
        if 0 <= x < self.current_room.width and 0 <= y < self.current_room.height:
            self.current_room.game_map[y][x] = game_object

    def current_room_is_finale(self) -> bool:
        return self.current_room.is_finale

    def get_height(self) -> int:
        return self.current_room.height

    def get_width(self) -> int:
        return self.current_room.width
