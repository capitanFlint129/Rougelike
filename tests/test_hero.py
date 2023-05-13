from unittest.mock import MagicMock

from state.enemy import Enemy
from state.actor import Actor
from state.hero import Hero


def test_hero_attack_actor():
    hero = Hero()
    actor = Enemy(1, 1)
    hero.attack(actor)
    assert actor.health == 9


def test_hero_attack_enemy_and_gain_experience():
    hero = Hero()
    hero.power = 10
    enemy = Enemy(1, 1)
    enemy.enemy_experience = MagicMock()
    enemy.enemy_experience.return_value = 1
    enemy.health = 1
    hero.attack(enemy)
    assert hero.experience == 1
    assert hero.health == 10


def test_hero_attack_enemy_and_not_gain_experience():
    hero = Hero()
    hero.power = 1
    enemy = Enemy(1, 1)
    enemy.enemy_experience = MagicMock()
    enemy.enemy_experience.return_value = 1
    enemy.health = 10
    hero.attack(enemy)
    assert hero.experience == 0


def test_hero_resurrect_player():
    hero = Hero()
    hero.is_alive = False
    hero.health = 0
    hero.resurrect_player()
    assert hero.is_alive
    assert hero.health == 10
