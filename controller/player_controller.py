from typing import Tuple

from controller.controller import Controller
from gui.command_handler import CommandHandler, UserCommand
from state.enemy import Enemy
from state.game_object import GameObject
from state.state import State
from state.item import Item
import state.physical_object as po


class PlayerController(Controller):
    """
    This class represents the controller for the player character in the game.
    It handles the player's movements and interactions with the game objects.
    """

    def __init__(self, command_handler: CommandHandler):
        self.command_handler = command_handler

    def update_state(self, game_state: State):
        """
        Updates the game state based on the player's actions.

        Args:
            game_state (State): The current state of the game.

        Return:
            None
        """
        next_x, next_y = self._get_next_coordinates(game_state.hero.coordinates)
        next_cell = game_state.game_map.get_object_at(next_x, next_y)

        self._handle_enemies(game_state, next_x, next_y)
        if game_state.hero.coordinates != (next_x, next_y):
            self._handle_map_objects(game_state, next_x, next_y, next_cell)

    def _get_next_coordinates(self, coordinates) -> Tuple:
        """
        Determines the next coordinates based on the user input.

        Args:
            coordinates (Coordinates): The current coordinates of the player character.

        Return:
            Tuple[int, int]: The next coordinates of the player character.
        """
        movement = {
            UserCommand.DOWN: (1, 0),
            UserCommand.UP: (-1, 0),
            UserCommand.RIGHT: (0, 1),
            UserCommand.LEFT: (0, -1),
        }
        command = self.command_handler.get_command()
        if command in movement:
            dy, dx = movement[command]
            return coordinates.x + dx, coordinates.y + dy

        return coordinates.x, coordinates.y

    @staticmethod
    def _handle_enemies(game_state: State, next_x: int, next_y: int) -> None:
        """
        Handles the player's interaction with an enemy.

        Args:
            game_state (State): The current state of the game.
            next_x (int): The x-coordinate of the next cell.
            next_y (int): The y-coordinate of the next cell.
        """
        for enemy in game_state.game_map.get_enemies():
            if enemy.coordinates == (next_x, next_y):
                game_state.hero.attack(enemy)
                return

    @staticmethod
    def _handle_map_objects(
        game_state: State, next_x: int, next_y: int, next_cell: GameObject
    ) -> None:
        """
        Handles the player's interaction with a game object.

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
