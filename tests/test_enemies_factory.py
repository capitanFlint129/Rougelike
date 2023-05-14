from generators.enemies_factory import *


def test_fantasy_enemy_factory():
    enemy_factory = FantasyEnemyFactory()
    map_array = [[None for j in range(10)] for i in range(10)]
    level = 1
    enemies = enemy_factory.create_enemies(level, map_array)
    assert len(enemies) == 1
    enemy = next(iter(enemies))
    assert isinstance(enemy, Enemy)


def test_scifi_enemy_factory():
    enemy_factory = SciFiEnemyFactory()
    map_array = [[None for j in range(10)] for i in range(10)]
    level = 1
    enemies = enemy_factory.create_enemies(level, map_array)
    assert len(enemies) == 1
    enemy = next(iter(enemies))
    assert isinstance(enemy, Enemy)
