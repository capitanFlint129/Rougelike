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
    Abstract class representing a builder interface for generating a game map.

    Attributes:
        room (Room): The game map room that is being built.
        level (int): The level of the game map being built.
    """

    def __init__(self, level: int = 1):
        """
        Initializes a new MapBuilderInterface object.

        Args:
            level (int): The level of the game map being built. Default is 1.
        """
        self.room = Room("")
        self.level = level

    def set_level(self, level: int):
        """
        Sets the level of the game map being built.

        Args:
            level (int): The level of the game map being built.
        """
        self.level = level

    def reset(self, level: int = 1):
        """
        Resets the builder to its initial state.

        Args:
            level (int): The level of the game map being built. Default is 1.
        """
        self.room, self.level = Room(""), level

    def get_room(self):
        """
        Returns the game map room that has been built.

        Returns:
            Room: The game map room that has been built.
        """
        return self.room

    @abstractmethod
    def generate_map(self, width: int, height: int):
        """
        Generates the game map.

        Args:
            width (int): The width of the game map.
            height (int): The height of the game map.
        """
        pass

    @abstractmethod
    def generate_enemies(self, enemies_factory: EnemyFactory):
        """
        Generates the enemies for the game map.

        Args:
            enemies_factory (EnemyFactory): The factory object used to create the enemies.
        """
        pass

    @abstractmethod
    def generate_items(self, items_generator: ItemGenerator):
        """
        Generates the items for the game map.

        Args:
            items_generator (ItemGenerator): The generator object used to create the items.
        """
        pass


class RandomMapBuilder(MapBuilderInterface):
    """
    Concrete builder class that generates a random game map.
    """

    def generate_map(self, width: int, height: int):
        """
        Generates a random game map.

        Args:
            width (int): The width of the game map.
            height (int): The height of the game map.
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

    def generate_enemies(self, enemies_factory: EnemyFactory):
        """
        Generates the enemies for the game map.

        Args:
            enemies_factory (EnemyFactory): The factory object used to create the enemies.
        """
        enemies = enemies_factory.create_en
