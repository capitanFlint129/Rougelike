from utils.coordinates import Coordinates
from state.enemy_strategy import (
    EnemyMovement,
    AggressiveEnemyStrategy,
    PassiveEnemyStrategy,
    PassiveAttackEnemyStrategy,
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


def test_passive_attack_enemy_strategy_get_next_coordinates_returns_player_coordinates_when_distance_is_one():
    strategy = PassiveAttackEnemyStrategy()
    enemy_coordinates = Coordinates(0, 0)
    player_coordinates = Coordinates(0, 1)
    next_coordinates = strategy.get_next_coordinates(
        enemy_coordinates, player_coordinates
    )
    assert next_coordinates == player_coordinates


def test_passive_attack_enemy_strategy_get_next_coordinates_returns_enemy_coordinates_when_distance_is_not_one():
    strategy = PassiveAttackEnemyStrategy()
    enemy_coordinates = Coordinates(0, 0)
    player_coordinates = Coordinates(1, 1)
    next_coordinates = strategy.get_next_coordinates(
        enemy_coordinates, player_coordinates
    )
    assert next_coordinates == enemy_coordinates


def test_passive_attack_enemy_strategy_get_next_coordinates_returns_enemy_coordinates_when_distance_is_greater_than_one():
    strategy = PassiveAttackEnemyStrategy()
    enemy_coordinates = Coordinates(0, 0)
    player_coordinates = Coordinates(3, 4)
    next_coordinates = strategy.get_next_coordinates(
        enemy_coordinates, player_coordinates
    )
    assert next_coordinates == enemy_coordinates
