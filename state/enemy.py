import random

from state.actor import Actor
from state.item import Item
from utils.coordinates import Coordinates
import state.enemy_strategy as es


class Enemy(Actor):
    """
    Represents an enemy character within a game. Inherits from the Actor class, and overrides the "get_icon" and
    "get_name" methods to provide the enemy's visual representation and name. The class also overrides the "equip" and
    "get_item" methods to prevent the enemy from equipping or picking up items.
    """

    def __init__(self, x=60, y=17):
        super(Enemy, self).__init__(x, y)
        self.movement_strategy = es.EnemyMovement()

    def get_icon(self):
        return "*"

    def get_name(self):
        return "enemy"

    def equip(self, item: Item):
        pass

    def get_item(self, item: Item):
        pass

    def enemy_experience(self) -> int:
        pass

    def move(self, player_coordinates: Coordinates) -> Coordinates:
        return self.movement_strategy.move(self.coordinates, player_coordinates)


class AggressiveEnemy(Enemy):
    def __init__(self, x=60, y=17):
        super().__init__(x, y)
        self.movement_strategy.set_strategy(es.AggressiveEnemyStrategy())

    def get_icon(self):
        return "A"

    def get_name(self):
        return "Aggressor"

    def enemy_experience(self) -> int:
        return 2


class DefensiveEnemy(Enemy):
    def __init__(self, x=60, y=17):
        super().__init__(x, y)
        self.movement_strategy.set_strategy(es.PassiveEnemyStrategy())

    def get_icon(self):
        return "D"

    def get_name(self):
        return "Defender"

    def enemy_experience(self) -> int:
        return 1


class CautiousEnemy(Enemy):
    def __init__(self, x=60, y=17):
        super().__init__(x, y)
        self.movement_strategy.set_strategy(es.CowardlyEnemyStrategy())

    def get_icon(self):
        return "C"

    def get_name(self):
        return "Cautious One"

    def enemy_experience(self) -> int:
        return 1
