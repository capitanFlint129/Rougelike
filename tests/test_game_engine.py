import pytest
from unittest.mock import MagicMock, patch
from game_engine.game_engine import GameEngine
from game_engine.commands import GameEngineCommandOk


@pytest.fixture
def mock_state():
    return MagicMock()


@pytest.fixture
def mock_controllers():
    return [MagicMock()]


@pytest.fixture
def mock_command_handler():
    return MagicMock()


@pytest.fixture
def mock_gui():
    return MagicMock()


@pytest.fixture
def mock_inventory_menu():
    return MagicMock()


def test_game_engine_run_game_over(
    mock_state, mock_controllers, mock_command_handler, mock_gui
):
    mock_state.lives = 0
    game_engine = GameEngine(
        mock_state, mock_controllers, mock_command_handler, mock_gui
    )
    mock_command_handler.get_command.side_effect = [None, GameEngineCommandOk()]
    with patch("time.sleep", return_value=None):
        game_engine.run()

    mock_gui.show_game_over_message.assert_called_once_with(mock_state.score)
    mock_command_handler.get_command.assert_called()


def test_game_engine_run_game_step(
    mock_state, mock_controllers, mock_command_handler, mock_gui
):
    mock_state.lives = 1
    mock_state.hero.health = 100
    mock_state.room_changed = False
    mock_command_handler.get_command.return_value = None
    game_engine = GameEngine(
        mock_state, mock_controllers, mock_command_handler, mock_gui
    )

    with patch("time.sleep", return_value=None):
        game_engine._run_game_step()

    for controller in mock_controllers:
        controller.update_state.assert_called_once_with(mock_state)
    mock_gui.update_display.assert_called_once()
