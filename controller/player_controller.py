from typing import Tuple

from controller.controller import Controller
from gui.command_handler import CommandHandler, UserCommand
from state.enemy import Enemy
from state.game_object import GameObject
from state.state import State
from state.item import Item
import state.physical_object as po


class PlayerController(Controller):
    def __init__(self, command_handler: CommandHandler):
        self.command_handler = command_handler

    def update_state(self, game_state: State):
        next_y, next_x = self._get_next_coordinates(game_state.hero.coordinates)
        next_cell = game_state.current_room.game_map[next_y][next_x]

        self._handle_enemies(game_state, next_y, next_x)
        self._handle_map_objects(game_state, next_y, next_x, next_cell)

    def _get_next_coordinates(self, coordinates) -> Tuple:
        movement = {
            UserCommand.DOWN: (1, 0),
            UserCommand.UP: (-1, 0),
            UserCommand.RIGHT: (0, 1),
            UserCommand.LEFT: (0, -1),
        }
        command = self.command_handler.get_command()
        if command in movement:
            dy, dx = movement[command]
            return coordinates.y + dy, coordinates.x + dx

        return coordinates.y, coordinates.x

    @staticmethod
    def _handle_enemies(game_state: State, next_y: int, next_x: int) -> None:
        for enemy in game_state.current_room.enemies:
            if enemy.coordinates == (next_x, next_y):
                game_state.hero.attack(enemy)
                return

    @staticmethod
    def _handle_map_objects(game_state: State, next_y: int, next_x: int, next_cell: GameObject) -> None:
        if isinstance(next_cell, (po.Wall, po.MapBorder, Enemy)):
            return

        game_state.hero.move_to(next_x, next_y)

        if isinstance(next_cell, po.Thorn):
            game_state.score = 0
            game_state.lives -= 1
        elif isinstance(next_cell, po.Coin):
            game_state.score += 1
            game_state.current_room.game_map[next_y][next_x] = po.FreeSpace()
        elif isinstance(next_cell, Item):
            print("item got")
            game_state.hero.equip(next_cell)
            game_state.current_room.game_map[next_y][next_x] = po.FreeSpace()
