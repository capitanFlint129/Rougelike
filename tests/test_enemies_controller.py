import pytest
from unittest.mock import MagicMock
from controller.enemies_controller import EnemiesController
from state.state import State
from state.hero import Hero
from state.enemy import Enemy
import state.physical_object as po
from utils.coordinates import Coordinates


@pytest.fixture
def mock_game_state():
    game_state = MagicMock()
    game_state.hero = MagicMock(spec=Hero)
    game_state.hero.coordinates = Coordinates(5, 5)
    game_state.game_map.get_map.return_value = [[po.FreeSpace() for _ in range(10)] for _ in range(10)]
    return game_state


@pytest.fixture
def mock_enemies():
    enemies = {MagicMock(spec=Enemy), MagicMock(spec=Enemy)}
    for enemy in enemies:
        enemy.is_alive = True
    return enemies


def test_enemies_controller_update_state_no_player_near(mock_game_state, mock_enemies):
    mock_game_state.game_map.get_enemies.return_value = mock_enemies

    for enemy in mock_enemies:
        enemy.coordinates = Coordinates(1, 1)

    enemies_controller = EnemiesController()
    enemies_controller.update_state(mock_game_state)

    for enemy in mock_enemies:
        enemy.attack.assert_not_called()
        enemy.move_to.assert_called_once()


def test_enemies_controller_update_state_player_near(mock_game_state, mock_enemies):
    mock_game_state.game_map.get_enemies.return_value = mock_enemies

    for enemy in mock_enemies:
        enemy.coordinates = Coordinates(4, 5)

    enemies_controller = EnemiesController()
    enemies_controller.update_state(mock_game_state)

    for enemy in mock_enemies:
        enemy.attack.assert_called_once_with(mock_game_state.hero)
        enemy.move_to.assert_not_called()


def test_enemies_controller_update_state_dead_enemies(mock_game_state, mock_enemies):
    mock_game_state.game_map.get_enemies.return_value = mock_enemies

    for enemy in mock_enemies:
        enemy.is_alive = False

    enemies_controller = EnemiesController()
    enemies_controller.update_state(mock_game_state)

    for enemy in mock_enemies:
        enemy.attack.assert_not_called()
        enemy.move_to.assert_not_called()

    assert mock_game_state.game_map.get_enemies.call_count == 1
