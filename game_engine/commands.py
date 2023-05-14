from abc import ABC

from state.state import State


class GameEngineCommand(ABC):
    """
    Abstract base class for game engine commands. All game engine commands must inherit from this class and
    implement the execute method.

    Args:
        ABC: Python Abstract Base Class

    Methods:
        execute(self, state: State): Executes the game engine command.

    Attributes:
        None
    """

    def execute(self, state: State):
        """
        Abstract method to be implemented by the child classes.

        Args:
            state (State): The current state of the game.
        """
        pass


class GameEngineCommandOpenInventory(GameEngineCommand):
    """
    A game engine command to open the inventory menu.

    Args:
        GameEngineCommand: The base class that this command inherits from.
        inventory_menu: The inventory menu object to be opened.

    Methods:
        execute(self, state: State): Executes the command to open the inventory menu.

    Attributes:
        inventory_menu: The inventory menu object to be opened.
    """

    def __init__(self, inventory_menu):
        self.inventory_menu = inventory_menu

    def execute(self, state: State):
        """
        Opens the inventory menu.

        Args:
            state (State): The current state of the game.
        """
        if state.lives != 0:
            self.inventory_menu.open()


class GameEngineCommandOk(GameEngineCommand):
    """
    A game engine command that does nothing.

    Args:
        GameEngineCommand: The base class that this command inherits from.

    Methods:
        execute(self, state: State): Executes the command to do nothing.

    Attributes:
        None
    """

    def execute(self, state: State):
        """
        Does nothing.

        Args:
            state (State): The current state of the game.
        """
        pass
