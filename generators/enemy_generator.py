from typing import List
import random
from state.enemy import Enemy


class EnemyGenerator:

    @staticmethod
    def generate_enemies(level: int, map_array: List):
        x = random.randint(3, len(map_array[0]) - 3)
        y = random.randint(3, len(map_array) - 3)
        return {Enemy(x, y)}
