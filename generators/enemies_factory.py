import random
from abc import ABC, abstractmethod
from typing import List, Set
from state.enemy import *
from state.game_object import GameObject


class EnemyFactory(ABC):
    """An abstract base class for enemy factories that create sets of enemies.

    Concrete subclasses of this class must implement the `create_enemies` method.
    """

    @abstractmethod
    def create_enemies(
        self, level: int, map_array: List[List[GameObject]]
    ) -> Set[Enemy]:
        pass


# TODO: Я хотел тут сделать какой-то конфиг файл с врагами (json, global value, [no]sql)
# select enemy from enemies e where e.type is SciFi and e.min_level <= level;


class FantasyEnemyFactory(EnemyFactory):
    """A concrete subclass of `EnemyFactory` that creates fantasy enemies."""

    def create_enemies(
        self, level: int, map_array: List[List[GameObject]]
    ) -> Set[Enemy]:
        """Creates a set of fantasy enemies.

        Args:
            level: An integer representing the level of the game.
            map_array: A list of lists representing the game map.

        Returns:
            A set of `Enemy` objects.
        """
        x = random.randint(3, len(map_array[0]) - 3)
        y = random.randint(3, len(map_array) - 3)
        enemies_dict = {
            0: Dragon,
            1: ShieldspikeTurtles,
            2: PanicPuffs,
            3: DemonSword,
        }
        enemy_type = random.randint(0, len(enemies_dict) - 1)
        return {enemies_dict[enemy_type](x, y)}


class SciFiEnemyFactory(EnemyFactory):
    """A concrete subclass of `EnemyFactory` that creates sci-fi enemies."""

    def create_enemies(
        self, level: int, map_array: List[List[GameObject]]
    ) -> Set[Enemy]:
        """Creates a set of sci-fi enemies.

        Args:
            level: An integer representing the level of the game.
            map_array: A list of lists representing the game map.

        Returns:
            A set of `Enemy` objects.
        """
        x = len(map_array[0]) // 2 - 2
        y = len(map_array) // 2 - 2
        enemies_dict = {
            0: CyborgChainsaw,
            1: PoisonousMold,
            2: BioShields,
            3: Cryonites,
        }
        enemy_type = random.randint(0, len(enemies_dict) - 1)
        return {enemies_dict[enemy_type](x, y)}
