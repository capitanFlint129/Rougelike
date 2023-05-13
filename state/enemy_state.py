from abc import ABC, abstractmethod

from utils.coordinates import Coordinates


class EnemyState(ABC):
    @abstractmethod
    def get_next_coordinates(
        self, enemy_coordinates: Coordinates, player_coordinates: Coordinates
    ) -> Coordinates:
        pass


class AggressiveEnemyState(EnemyState):
    def get_next_coordinates(
        self, enemy_coordinates: Coordinates, player_coordinates: Coordinates
    ) -> Coordinates:
        def sign(x):
            return -1 if x < 0 else (1 if x > 0 else 0)

        dx = sign(player_coordinates.x - enemy_coordinates.x)
        dy = sign(player_coordinates.y - enemy_coordinates.y)

        return Coordinates(enemy_coordinates.x + dx, enemy_coordinates.y + dy)


class PassiveEnemyState(EnemyState):
    def get_next_coordinates(
        self, enemy_coordinates: Coordinates, player_coordinates: Coordinates
    ) -> Coordinates:
        return enemy_coordinates


class CowardlyEnemyState(EnemyState):
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
    def __init__(self, state=None):
        self.state = state

    def set_state(self, strategy: EnemyState):
        self.state = strategy

    def move(
        self, enemy_coordinates: Coordinates, player_coordinates: Coordinates
    ) -> Coordinates:
        return self.state.get_next_coordinates(enemy_coordinates, player_coordinates)
