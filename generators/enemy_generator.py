from typing import List, Set
import random
from state.enemy import Enemy


class EnemyGenerator:
    """
    Generate Enemies on the map.
    TODO: rewrite the generation algorithm in the future
    """

    @staticmethod
    def generate_enemies(level: int, map_array: List) -> Set[Enemy]:
        x = random.randint(3, len(map_array[0]) - 3)
        y = random.randint(3, len(map_array) - 3)
        return {Enemy(x, y)}
