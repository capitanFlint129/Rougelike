from typing import Optional

import keyboard

from controller.player_controller.commands import (
    PlayerControllerCommandUp,
    PlayerControllerCommandLeft,
    PlayerControllerCommandDown,
    PlayerControllerCommandRight,
    PlayerControllerCommand,
)
from game_engine.commands import GameEngineCommand, OpenInventoryCommand, OkCommand
from game_engine.inventory_menu.commands import (
    MenuCommand,
    MenuCommandUp,
    MenuCommandDown,
    MenuCommandApply,
    MenuCommandClose,
)


class PlayerControllerCommandHandler:
    """
    A class that handles user commands in the game.

    Methods:
        get_command: Returns the user command based on the currently pressed keyboard keys.
    """

    def get_command(self) -> Optional[PlayerControllerCommand]:
        if keyboard.is_pressed("w"):
            return PlayerControllerCommandUp()
        elif keyboard.is_pressed("s"):
            return PlayerControllerCommandDown()
        elif keyboard.is_pressed("a"):
            return PlayerControllerCommandLeft()
        elif keyboard.is_pressed("d"):
            return PlayerControllerCommandRight()
        return None


class GameEngineCommandHandler:
    """
    A class that handles user commands in the game.

    Methods:
        get_command: Returns the user command based on the currently pressed keyboard keys.
    """

    def __init__(
        self,
        inventory_menu,
    ):
        self.inventory_menu = inventory_menu

    def get_command(self) -> Optional[GameEngineCommand]:
        if keyboard.is_pressed("i"):
            return OpenInventoryCommand(self.inventory_menu)
        elif keyboard.is_pressed("e"):
            return OkCommand()
        return None


class InventoryMenuCommandHandler:
    """
    A class that handles user commands in the game.

    Methods:
        get_command: Returns the user command based on the currently pressed keyboard keys.
    """

    def get_command(self) -> Optional[MenuCommand]:
        if keyboard.is_pressed("w"):
            return MenuCommandUp()
        elif keyboard.is_pressed("s"):
            return MenuCommandDown()
        elif keyboard.is_pressed("e"):
            return MenuCommandApply()
        elif keyboard.is_pressed("i"):
            return MenuCommandClose()
        return None
