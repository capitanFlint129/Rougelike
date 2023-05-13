from utils.coordinates import Coordinates


class EnemyStrategy:
    def get_next_coordinates(
        self, enemy_coordinates: Coordinates, player_coordinates: Coordinates
    ) -> Coordinates:
        pass


class AggressiveEnemyStrategy(EnemyStrategy):
    def get_next_coordinates(
        self, enemy_coordinates: Coordinates, player_coordinates: Coordinates
    ) -> Coordinates:
        def sign(x):
            return -1 if x < 0 else (1 if x > 0 else 0)

        dx = sign(player_coordinates.x - enemy_coordinates.x)
        dy = sign(player_coordinates.y - enemy_coordinates.y)

        return Coordinates(enemy_coordinates.x + dx, enemy_coordinates.y + dy)


class PassiveEnemyStrategy(EnemyStrategy):
    def get_next_coordinates(
        self, enemy_coordinates: Coordinates, player_coordinates: Coordinates
    ) -> Coordinates:
        return enemy_coordinates


class PassiveAttackEnemyStrategy(EnemyStrategy):
    def get_next_coordinates(
        self, enemy_coordinates: Coordinates, player_coordinates: Coordinates
    ) -> Coordinates:
        if enemy_coordinates.distance(player_coordinates) == 1:
            return player_coordinates
        return enemy_coordinates


class CowardlyEnemyStrategy(EnemyStrategy):
    def get_next_coordinates(
        self, enemy_coordinates: Coordinates, player_coordinates: Coordinates
    ) -> Coordinates:
        if enemy_coordinates.distance(player_coordinates) >= 8:
            return enemy_coordinates

        def sign(x):
            return -1 if x < 0 else (1 if x > 0 else 0)

        dx = sign(player_coordinates.x - enemy_coordinates.x)
        dy = sign(player_coordinates.y - enemy_coordinates.y)

        return Coordinates(enemy_coordinates.x - dx, enemy_coordinates.y - dy)


class EnemyMovement:
    def __init__(self, strategy=None):
        self.strategy = strategy

    def set_strategy(self, strategy: EnemyStrategy):
        self.strategy = strategy

    def move(
        self, enemy_coordinates: Coordinates, player_coordinates: Coordinates
    ) -> Coordinates:
        return self.strategy.get_next_coordinates(enemy_coordinates, player_coordinates)
