from typing import Optional

import keyboard

from controller.player_controller.commands import *
from game_engine.commands import GameEngineCommand, OpenInventoryCommand, OkCommand
from game_engine.inventory_menu.commands import *


class PlayerControllerCommandHandler:
    """
    A class that handles user commands in the game.

    Methods:
        get_command: Returns the user command based on the currently pressed keyboard keys.
    """

    def get_command(self) -> Optional[GameCommand]:
        if keyboard.is_pressed("w"):
            return GameCommandUp()
        elif keyboard.is_pressed("s"):
            return GameCommandDown()
        elif keyboard.is_pressed("a"):
            return GameCommandLeft()
        elif keyboard.is_pressed("d"):
            return GameCommandRight()
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
