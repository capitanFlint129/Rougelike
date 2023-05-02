from typing import Set, List
import random
import state.item as items


class ItemGenerator:
    @staticmethod
    def generate_items(level: int, map_array: List) -> None:
        x = random.randint(3, len(map_array[0]) - 3)
        y = random.randint(3, len(map_array) - 3)
        item_id = random.randint(0, 6)
        if item_id == 0:
            map_array[y][x] = items.Sword()
        if item_id == 1:
            map_array[y][x] = items.Shield()
