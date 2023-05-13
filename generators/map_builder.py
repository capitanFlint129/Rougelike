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
    """
    Abstract base class for map builders.
    """

    def __init__(self, level: int = 1):
        """
        Initializes a new MapBuilderInterface.

        Args:
            level: The level of the map being built.
        """
        self.room = Room("")
        self.level = level

    def set_level(self, level: int):
        """
        Sets the level of the map being built.

        Args:
            level: The level of the map being built.
        """
        self.level = level

    def reset(self, level: int = 1):
        """
        Resets the builder.

        Args:
            level: The level of the map being built.
        """
        self.room, self.level = Room(""), level

    def get_room(self):
        """
        Returns the built room.

        Returns:
            The built room.
        """
        return self.room

    @abstractmethod
    def generate_map(self, width: int, height: int):
        """
        Generates the map.

        Args:
            width: The width of the map.
            height: The height of the map.
        """
        pass

    @abstractmethod
    def generate_enemies(self, enemies_factor: EnemyFactory):
        """
        Generates the enemies.

        Args:
            enemies_factor: The enemy factory.
        """
        pass

    @abstractmethod
    def generate_items(self, items_generator: ItemGenerator):
        """
        Generates the items.

        Args:
            items_generator: The item generator.
        """
        pass


class RandomMapBuilder(MapBuilderInterface):
    """
    A random map builder.
    """

    def generate_map(self, width: int, height: int):
        """
        Generates a random map.

        Args:
            width: The width of the map.
            height: The height of the map.
        """
        self.room = Room("")
        game_map = [
            ["#" if random.randint(0, 100) == 0 else " " for _ in range(width)]
            for _ in range(height)
        ]
        game_map[height - 1] = game_map[0] = ["#" for _ in range(width)]

        for i in range(height):
            game_map[i][0] = game_map[i][width - 1] = "#"

        game_map = [[get_physical_object(c) for c in row] for row in game_map]
        self.room.game_map = game_map
        self.room.width = width
        self.room.height = height

    def generate_enemies(self, enemies_factor: EnemyFactory):
        """
        Generates the enemies.

        Args:
            enemies_factor: The enemy factory.
        """
        enemies = enemies_factor.create_enemies(self.level, self.room.game_map)
        self.room.enemies = enemies

    def generate_items(self, items_generator: ItemGenerator):
        """
        Generates the items.

        Args:
            items_generator: The item generator.
        """
        items_generator.generate_items(self.level, self.room.game_map)


class FinalRoomBuilder(MapBuilderInterface):
    """
    A final room builder.
    """

    def generate_map(self, width: int = 0, height: int = 0):
        """
        Generates the final room map.

        Args:
            width: The width of the map.
            height: The height of the map.
        """

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
    """
    The MapDirector class is responsible for building and returning a Room object by using the provided
    MapBuilderInterface, EnemyFactory, and ItemGenerator objects.

    Attributes:
    builder (MapBuilderInterface): The builder object that will be used to build the Room.
    enemy_factory (EnemyFactory): The EnemyFactory object that will be used to generate enemies.
    item_generator (ItemGenerator): The ItemGenerator object that will be used to generate items.
    """

    def __init__(self):
        self.builder = RandomMapBuilder()
        self.enemy_factory = None
        self.item_generator = ItemGenerator()

    def set_builder(self, builder: MapBuilderInterface) -> None:
        """
        Set the MapBuilderInterface object to be used to build the Room.

        Args:
        builder (MapBuilderInterface): The MapBuilderInterface object that will be used to build the Room.

        Returns:
        None
        """
        self.builder = builder

    def set_enemy_factory(self, enemy_factory: EnemyFactory) -> None:
        """
        Set the EnemyFactory object to be used to generate enemies.

        Args:
        enemy_factory (EnemyFactory): The EnemyFactory object that will be used to generate enemies.

        Returns:
        None
        """
        self.enemy_factory = enemy_factory

    def set_item_generator(self, item_generator: ItemGenerator) -> None:
        """
        Set the ItemGenerator object to be used to generate items.

        Args:
        item_generator (ItemGenerator): The ItemGenerator object that will be used to generate items.

        Returns:
        None
        """
        self.item_generator = item_generator

    def build_room(self, width: int = 45, height: int = 25) -> Room:
        """
        Build and return a Room object.

        Args:
        width (int): The width of the room.
        height (int): The height of the room.

        Returns:
        Room: The Room object that was built.
        """
        self.builder.generate_map(width, height)
        self.builder.generate_enemies(self.enemy_factory)
        self.builder.generate_items(self.item_generator)
        room = self.builder.room
        self.builder.reset()
        return room
