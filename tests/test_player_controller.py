import pytest
from unittest.mock import MagicMock
from controller.player_controller import PlayerController
from gui.command_handler import CommandHandler, UserCommand
import state.physical_object as po
from state.item import Item
from utils.coordinates import Coordinates


@pytest.fixture
def mock_command_handler():
    ch = MagicMock(spec=CommandHandler)
    ch.get_command.return_value = None
    return ch


@pytest.fixture
def mock_game_state():
    state = MagicMock()
    state.hero.coordinates = Coordinates(5, 5)
    state.game_map.get_object_at.return_value = po.FreeSpace()
    return state


def test_player_controller_update_state_no_command(mock_command_handler, mock_game_state):
    player_controller = PlayerController(mock_command_handler)
    player_controller.update_state(mock_game_state)

    mock_game_state.hero.move_to.assert_not_called()


def test_player_controller_update_state_valid_command(mock_command_handler, mock_game_state):
    player_controller = PlayerController(mock_command_handler)
    mock_command_handler.get_command.return_value = UserCommand.RIGHT

    player_controller.update_state(mock_game_state)

    mock_game_state.hero.move_to.assert_called_once_with(6, 5)


def test_player_controller_update_state_wall(mock_command_handler, mock_game_state):
    player_controller = PlayerController(mock_command_handler)
    mock_command_handler.get_command.return_value = UserCommand.UP
    mock_game_state.game_map.get_object_at.return_value = po.Wall()

    player_controller.update_state(mock_game_state)

    mock_game_state.hero.move_to.assert_not_called()


def test_player_controller_update_state_item(mock_command_handler, mock_game_state):
    player_controller = PlayerController(mock_command_handler)
    mock_command_handler.get_command.return_value = UserCommand.DOWN
    item = MagicMock(spec=Item)
    mock_game_state.game_map.get_object_at.return_value = item

    player_controller.update_state(mock_game_state)

    mock_game_state.hero.inventory.add.assert_called_once_with(item)
    # (5, 6, <state.physical_object.FreeSpace object at 0x0000022842BD4070>)
    # != (5, 6, <state.physical_object.FreeSpace object at 0x0000022842BD9EA0>)
    # so use just called_once
    mock_game_state.game_map.set_object_at.assert_called_once()  # _with(5, 6, po.FreeSpace())
