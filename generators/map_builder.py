from abc import ABC, abstractmethod
import random
from typing import Optional

from state.enemy import Dragon
from state.item import Sword
from state.physical_object_factory import get_physical_object
from state.game_map import Room
from generators.enemies_factory import EnemyFactory
from generators.item_generator import ItemGenerator


class MapBuilderInterface(ABC):

    def __init__(self, level: int = 1):
        self.room = Room("")
        self.level = level

    def set_level(self, level: int):
        self.level = level

    def reset(self, level: int = 1):
        self.room, self.level = Room(""), level

    def get_room(self):
        return self.room

    @abstractmethod
    def generate_map(self, width: int, height: int):
        pass

    @abstractmethod
    def generate_enemies(self, enemies_factor: EnemyFactory):
        pass

    @abstractmethod
    def generate_items(self, items_generator: ItemGenerator):
        pass


class RandomMapBuilder(MapBuilderInterface):
    def generate_map(self, width: int, height: int):
        self.room = Room("")
        game_map = [['#' if random.randint(0, 100) == 0 else ' ' for _ in range(width)] for _ in range(height)]
        game_map[height - 1] = game_map[0] = ['#' for _ in range(width)]

        for i in range(height):
            game_map[i][0] = game_map[i][width - 1] = '#'

        game_map = [[get_physical_object(c) for c in row] for row in game_map]
        self.room.game_map = game_map
        self.room.width = width
        self.room.height = height

    def generate_enemies(self, enemies_factor: EnemyFactory):
        enemies = enemies_factor.create_enemies(self.level, self.room.game_map)
        self.room.enemies = enemies

    def generate_items(self, items_generator: ItemGenerator):
        items_generator.generate_items(self.level, self.room.game_map)


#
class FinalRoomBuilder(MapBuilderInterface):
    def generate_map(self, width: int = 0, height: int = 0):
        with open(f"levels/level_{self.level}.txt", "r") as levels_file:
            game_map = [list(line.strip()) for line in levels_file.readlines()]
            game_map = [[get_physical_object(c) for c in row] for row in game_map]
        self.room = Room("")
        self.room.game_map = game_map
        self.room.height = len(game_map)
        self.room.width = len(game_map[0])
        self.room.is_finale = True

    def generate_enemies(self, enemies_factor: Optional[EnemyFactory] = None):
        self.room.enemies = {Dragon(60, 17)}

    def generate_items(self, items_generator: Optional[ItemGenerator] = None):
        self.room.game_map[20][10] = Sword()


class MapDirector:
    def __init__(self):
        self.builder = RandomMapBuilder()
        self.enemy_factory = None
        self.item_generator = ItemGenerator()

    def set_builder(self, builder: MapBuilderInterface):
        self.builder = builder

    def set_enemy_factory(self, enemy_factory: EnemyFactory):
        self.enemy_factory = enemy_factory

    def set_item_generator(self, item_generator: ItemGenerator):
        self.item_generator = item_generator

    def build_room(self, width: int = 45, height: int = 25) -> Room:
        self.builder.generate_map(width, height)
        self.builder.generate_enemies(self.enemy_factory)
        self.builder.generate_items(self.item_generator)
        room = self.builder.room
        self.builder.reset()
        return room
