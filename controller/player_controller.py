from controller.controller import Controller
from gui.command_handler import CommandHandler, UserCommand
from state.enemy import Enemy
from state.state import State
import state.physical_object as po


class PlayerController(Controller):
    def __init__(self, command_handler: CommandHandler):
        self.command_handler = command_handler

    def update_state(self, game_state: State):
        command = self.command_handler.get_command()
        coordinates = game_state.hero.coordinates

        player = game_state.hero
        game_map = game_state.current_room.game_map

        if command == UserCommand.DOWN:
            next_y, next_x = coordinates.y + 1, coordinates.x
        elif command == UserCommand.UP:
            next_y, next_x = coordinates.y - 1, coordinates.x
        elif command == UserCommand.RIGHT:
            next_y, next_x = coordinates.y, coordinates.x + 1
        elif command == UserCommand.LEFT:
            next_y, next_x = coordinates.y, coordinates.x - 1
        else:
            next_y, next_x = coordinates.y, coordinates.x

        next_cell = game_map[next_y][next_x]
        enemies = game_state.current_room.enemies
        for enemy in enemies:
            if enemy.coordinates.x == next_x and enemy.coordinates.y == next_y:
                player.attack(enemy)
                return

        if isinstance(next_cell, po.Wall) or isinstance(next_cell, po.MapBorder):
            return

        game_state.hero.move_to(next_x, next_y)
        if isinstance(next_cell, po.Thorn):
            game_state.score = 0
            game_state.lives -= 1
        if isinstance(next_cell, po.Coin):
            game_state.score += 1
            game_map[next_y][next_x] = po.FreeSpace
