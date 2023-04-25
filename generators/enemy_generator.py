from typing import List
import random
from state.enemy import Enemy


class EnemyGenerator:

    @staticmethod
    def generate_enemies(level: int, map_array: List):
        x = random.randint(2, len(map_array) - 2)
        y = random.randint(2, len(map_array[0]) - 2)
        return Enemy(x, y)
