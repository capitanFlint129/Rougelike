from typing import List, Set
import random
import state.enemy as enemies


class EnemyGenerator:
    """
    Generate Enemies on the map.
    TODO: rewrite the generation algorithm in the future
    """

    @staticmethod
    def generate_enemies(level: int, map_array: List) -> Set[enemies.Enemy]:
        x = random.randint(3, len(map_array[0]) - 3)
        y = random.randint(3, len(map_array) - 3)
        enemy_type = random.randint(0, 2)
        enemies_dict = {0: enemies.AggressiveEnemy,
                        1: enemies.DefensiveEnemy,
                        2: enemies.CautiousEnemy}
        return {enemies_dict[enemy_type](x, y)}
