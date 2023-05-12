from abc import ABC, abstractmethod
from typing import Tuple

import state.physical_object as po
from state.enemy import Enemy
from state.game_object import GameObject
from state.item import Item
from state.state import State


class PlayerControllerCommandsFactory:
    def create_command_up(self):
        return GameCommandUp()

    def create_command_down(self):
        return GameCommandDown()

    def create_command_left(self):
        return GameCommandLeft()

    def create_command_right(self):
        return GameCommandRight()


class GameCommand(ABC):
    def execute(self, state: State):
        next_x, next_y = self._get_next_coordinates(state.hero.coordinates)
        next_cell = state.game_map.get_object_at(next_x, next_y)

        enemy_attacked = self._handle_enemies(state, next_x, next_y)
        if not enemy_attacked and state.hero.coordinates != (next_x, next_y):
            self._handle_map_objects(state, next_x, next_y, next_cell)

    def _get_next_coordinates(self, coordinates) -> Tuple:
        """
        Determines the next coordinates based on the user input.

        Args:
            coordinates (Coordinates): The current coordinates of the player character.

        Return:
            Tuple[int, int]: The next coordinates of the player character.
        """
        dy, dx = self._get_movement()
        return coordinates.x + dx, coordinates.y + dy

    @abstractmethod
    def _get_movement(self):
        pass

    @staticmethod
    def _handle_enemies(game_state: State, next_x: int, next_y: int) -> bool:
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
                return True
        return False

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


class GameCommandUp(GameCommand):
    def _get_movement(self):
        return -1, 0


class GameCommandDown(GameCommand):
    def _get_movement(self):
        return 1, 0


class GameCommandLeft(GameCommand):
    def _get_movement(self):
        return 0, -1


class GameCommandRight(GameCommand):
    def _get_movement(self):
        return 0, 1
