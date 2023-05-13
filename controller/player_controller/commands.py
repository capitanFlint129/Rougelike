from abc import ABC, abstractmethod
from typing import Tuple

import state.physical_object as po
from state.enemy import Enemy
from state.game_object import GameObject
from state.item import Item
from state.state import State


class PlayerControllerCommand(ABC):
    """An abstract base class for player controller commands."""

    @abstractmethod
    def execute(self, state: State):
        """Executes the player controller command.

        Args:
            state (State): The current state of the game.
        """

    def _get_next_coordinates(self, coordinates) -> Tuple:
        """Determines the next coordinates based on the user input.

        Args:
            coordinates (Coordinates): The current coordinates of the player character.

        Return:
            Tuple[int, int]: The next coordinates of the player character.
        """
        dy, dx = self._get_movement()
        return coordinates.x + dx, coordinates.y + dy

    @abstractmethod
    def _get_movement(self):
        """Gets the movement for the player controller command."""


    @staticmethod
    def _handle_enemies(game_state: State, next_x: int, next_y: int) -> bool:
        """Handles the player's interaction with an enemy.

        Args:
            game_state (State): The current state of the game.
            next_x (int): The x-coordinate of the next cell.
            next_y (int): The y-coordinate of the next cell.

        Returns:
            bool: True if the player attacked an enemy, False otherwise.
        """
        for enemy in game_state.game_map.get_enemies():
            if enemy.coordinates == (next_x, next_y):
                game_state.hero.attack(enemy)
                return True
        return False

    @staticmethod
    def _handle_map_objects(
        game_state: State, next_x: int, next_y: int, next_cell: GameObject
    ) -> None:
        """Handles the player's interaction with a game object.

        Args:
            game_state (State): The current state of the game.
            next_x (int): The x-coordinate of the next cell.
            next_y (int): The y-coordinate of the next cell.
            next_cell (GameObject): The object in the next cell.
        """
        if isinstance(next_cell, (po.Wall, po.MapBorder, Enemy)):
            return

        game_state.hero.move_to(next_x, next_y)

        if isinstance(next_cell, po.Thorn):
            game_state.score = 0
            game_state.lives -= 1
        elif isinstance(next_cell, po.Coin):
            game_state.score += 1
            game_state.game_map.set_object_at(next_x, next_y, po.FreeSpace())
        elif isinstance(next_cell, Item):
            game_state.hero.inventory.add(next_cell)
            game_state.game_map.set_object_at(next_x, next_y, po.FreeSpace())


class PlayerControllerCommandUp(PlayerControllerCommand):
    """A player controller command to move the player character up."""

    def _get_movement(self):
        """Gets the movement for moving up.

        Returns:
            Tuple[int, int]: The movement in the x and y direction.
        """
        return -1, 0


class PlayerControllerCommandDown(PlayerControllerCommand):
    """A player controller command to move the player character down."""

    def _get_movement(self):
        """Gets the movement for moving down.

        Returns:
            Tuple[int, int]: The movement in the x and y direction.
        """
        return 1, 0


class PlayerControllerCommandLeft(PlayerControllerCommand):
    """A command that moves the player character left by one cell."""

    def _get_movement(self):
        """
        Determines the movement vector for moving the player character left.

        Return:
            Tuple[int, int]: The movement vector.
        """
        return 0, -1


class PlayerControllerCommandRight(PlayerControllerCommand):
    """A command that moves the player character right by one cell."""

    def _get_movement(self):
        """
        Determines the movement vector for moving the player character right.

        Return:
            Tuple[int, int]: The movement vector.
        """
        return 0, 1
