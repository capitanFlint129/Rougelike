from abc import ABC, abstractmethod

from utils.coordinates import Coordinates


class EnemyState(ABC):
    """
    A base class for implementing enemy strategies in a game.
    """

    @abstractmethod
    def get_next_coordinates(
        self, enemy_coordinates: Coordinates, player_coordinates: Coordinates
    ) -> Coordinates:
        pass


class AggressiveEnemyState(EnemyState):
    """
    A class for implementing aggressive enemy strategy in a game.
    """

    def get_next_coordinates(
        self, enemy_coordinates: Coordinates, player_coordinates: Coordinates
    ) -> Coordinates:
        def sign(x):
            return -1 if x < 0 else (1 if x > 0 else 0)

        dx = sign(player_coordinates.x - enemy_coordinates.x)
        dy = sign(player_coordinates.y - enemy_coordinates.y)

        return Coordinates(enemy_coordinates.x + dx, enemy_coordinates.y + dy)


class PassiveEnemyState(EnemyState):
    """
    A class for implementing passive enemy strategy in a game.
    """

    def get_next_coordinates(
        self, enemy_coordinates: Coordinates, player_coordinates: Coordinates
    ) -> Coordinates:
        return enemy_coordinates


class PassiveAttackEnemyState(EnemyState):
    """
    A class for implementing the passive strategy of the
    enemy, with attacks on neighboring cells
    """

    def get_next_coordinates(
        self, enemy_coordinates: Coordinates, player_coordinates: Coordinates
    ) -> Coordinates:
        if enemy_coordinates.distance(player_coordinates) == 1:
            return player_coordinates
        return enemy_coordinates


class CowardlyEnemyState(EnemyState):
    """
    A class for implementing cowardly enemy strategy in a game.
    """

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
    """
    A class for moving an enemy in a game.

    :Attributes:
        - `strategy`: An instance of an EnemyStrategy subclass that defines the strategy for enemy movement.
    """

    def __init__(self, state=None):
        self.state = state

    def set_state(self, strategy: EnemyState):
        """
        Sets the strategy for enemy movement
        """
        self.state = strategy

    def move(
        self, enemy_coordinates: Coordinates, player_coordinates: Coordinates
    ) -> Coordinates:
        """
        Returns the next coordinates of the enemy based on the strategy.
        """
        return self.state.get_next_coordinates(enemy_coordinates, player_coordinates)
