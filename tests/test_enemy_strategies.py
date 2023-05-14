from utils.coordinates import Coordinates
from state.enemy_strategy import (
    EnemyMovement,
    AggressiveEnemyStrategy,
    PassiveEnemyStrategy,
    CowardlyEnemyStrategy,
)


def test_aggressive_enemy_strategy():
    movement = EnemyMovement(AggressiveEnemyStrategy())
    enemy_coords = Coordinates(2, 2)
    player_coords = Coordinates(6, 6)
    next_coords = movement.move(enemy_coords, player_coords)
    assert next_coords == Coordinates(3, 3)


def test_passive_enemy_strategy():
    movement = EnemyMovement(PassiveEnemyStrategy())
    enemy_coords = Coordinates(2, 2)
    player_coords = Coordinates(6, 6)
    next_coords = movement.move(enemy_coords, player_coords)
    assert next_coords == Coordinates(2, 2)


def test_cowardly_enemy_strategy():
    movement = EnemyMovement(CowardlyEnemyStrategy())
    enemy_coords = Coordinates(2, 2)
    player_coords = Coordinates(6, 6)
    next_coords = movement.move(enemy_coords, player_coords)
    assert next_coords == Coordinates(1, 1)
