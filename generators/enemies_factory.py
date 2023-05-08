import random
from abc import ABC, abstractmethod
from typing import List, Set
from state.enemy import *
from state.game_object import GameObject


class EnemyFactory(ABC):
    @abstractmethod
    def create_enemies(self, level: int, map_array: List[List[GameObject]]) -> Set[Enemy]:
        pass


# TODO: Я хотел тут сделать какой-то конфиг файл с врагами (json, global value, [no]sql)
# select enemy from enemies e where e.type is SciFi and e.min_level <= level;

class FantasyEnemyFactory(EnemyFactory):
    def create_enemies(self, level: int, map_array: List[List[GameObject]]) -> Set[Enemy]:
        x = random.randint(3, len(map_array[0]) - 3)
        y = random.randint(3, len(map_array) - 3)
        enemies_dict = {
            0: Dragon,
            1: ShieldspikeTurtles,
            2: PanicPuffs
        }
        enemy_type = random.randint(0, len(enemies_dict) - 1)
        return {enemies_dict[enemy_type](x, y)}


class SciFiEnemyFactory(EnemyFactory):
    def create_enemies(self, level: int, map_array: List[List[GameObject]]) -> Set[Enemy]:
        x = len(map_array[0]) // 2 - 2
        y = len(map_array) // 2 - 2
        enemies_dict = {
            0: CyborgChainsaw,
            1: LaserShark,
            2: BioShields,
            3: Cryonites
        }
        enemy_type = random.randint(0, len(enemies_dict) - 1)
        return {enemies_dict[enemy_type](x, y)}
