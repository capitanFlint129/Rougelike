import pytest
from unittest.mock import MagicMock
from controller import WorldController
from state.hero import Hero
import state.physical_object as po
from utils.coordinates import Coordinates


@pytest.fixture
def mock_game_state():
    game_state = MagicMock()
    game_state.hero = MagicMock(spec=Hero)
    game_state.hero.coordinates = Coordinates(5, 5)
    return game_state


def test_world_controller_update_state_dead_hero(mock_game_state):
    mock_game_state.hero.is_alive = False
    mock_game_state.lives = 5
    world_controller = WorldController()
    world_controller.new_level = MagicMock()

    world_controller.update_state(mock_game_state)

    assert mock_game_state.lives == 4
    mock_game_state.hero.resurrect_player.assert_called_once()
    world_controller.new_level.assert_called_once_with(mock_game_state)


def test_world_controller_update_state_level_completion(mock_game_state):
    mock_game_state.hero.is_alive = True
    mock_game_state.game_map.current_room_is_finale.return_value = True
    mock_game_state.game_map.get_object_at.return_value = po.ExitPortal()
    world_controller = WorldController()
    world_controller.handle_level_completion = MagicMock()

    world_controller.update_state(mock_game_state)

    world_controller.handle_level_completion.assert_called_once_with(mock_game_state)


def test_world_controller_update_state_door_transition(mock_game_state):
    mock_game_state.hero.is_alive = True
    mock_game_state.game_map.current_room_is_finale.return_value = False
    mock_game_state.game_map.get_object_at.return_value = po.Door()
    world_controller = WorldController()
    world_controller.handle_door_transition = MagicMock()

    world_controller.update_state(mock_game_state)

    world_controller.handle_door_transition.assert_called_once_with(
        mock_game_state, mock_game_state.hero.get_x(), mock_game_state.hero.get_y()
    )
