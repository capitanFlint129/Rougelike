from unittest.mock import Mock
from unittest.mock import patch
import pytest
import keyboard

from game_engine.inventory_menu.commands import (
    MenuCommandUp,
    MenuCommandDown,
    MenuCommandApply,
    MenuCommandClose,
)
from game_engine.inventory_menu.menu_state import MenuState
from gui.command_handler import InventoryMenuCommandHandler
from game_engine.inventory_menu.inventory_menu import InventoryMenu


class TestMenuCommand:
    @pytest.fixture
    def menu_state(self):
        hero = Mock()
        items_list = ["item1", "item2"]
        equipped = ["item1"]
        return MenuState(hero, items_list, equipped)

    def test_menu_command_up(self, menu_state):
        command = MenuCommandUp()
        assert menu_state.user_position == 0
        command.execute(menu_state)
        assert menu_state.user_position == 0
        command.execute(menu_state)
        assert menu_state.user_position == 0
        menu_state.user_position = 1
        command.execute(menu_state)
        assert menu_state.user_position == 0

    def test_menu_command_down(self, menu_state):
        command = MenuCommandDown()
        assert menu_state.user_position == 0
        command.execute(menu_state)
        assert menu_state.user_position == 1
        command.execute(menu_state)
        assert menu_state.user_position == 1
        menu_state.user_position = 0
        command.execute(menu_state)
        assert menu_state.user_position == 1

    def test_menu_command_close(self, menu_state):
        command = MenuCommandClose()
        assert menu_state.is_open
        command.execute(menu_state)
        assert not menu_state.is_open
