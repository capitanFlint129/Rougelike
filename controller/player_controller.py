from controller.controller import Controller
from gui.command_handler import CommandHandler, UserCommand
from state.enemy import Enemy
from state.item import Item
from state.state import State


class PlayerController(Controller):
    def __init__(self, command_handler: CommandHandler):
        self.command_handler = command_handler

    def update_state(self, game_state: State):
        command = self.command_handler.get_command()
        next_y = game_state.player_y
        next_x = game_state.player_x
        game_state.level[game_state.player_y][game_state.player_x] = ""
        if command == UserCommand.DOWN:
            next_y, next_x = game_state.player_y + 1, game_state.player_x
        elif command == UserCommand.UP:
            next_y, next_x = game_state.player_y - 1, game_state.player_x
        elif command == UserCommand.RIGHT:
            next_y, next_x = game_state.player_y, game_state.player_x + 1
        elif command == UserCommand.LEFT:
            next_y, next_x = game_state.player_y, game_state.player_x - 1

        next_cell = game_state.level[next_y][next_x]
        if isinstance(next_cell, Enemy):
            game_state.hero.attack(next_cell)
        elif not next_cell == "#":
            if isinstance(next_cell, Item):
                game_state.hero.get_item(next_cell)
            game_state.player_y = next_y
            game_state.player_x = next_x
            if next_cell in ["^", ">", "v", "<"]:
                game_state.score = 0
                game_state.lives -= 1
            if next_cell == "c":
                game_state.score += 1
                game_state.level[next_y][next_x] = ""
            if next_cell == "H":
                game_state.lives += 1
                game_state.level[next_y][next_x] = ""
        game_state.level[game_state.player_y][game_state.player_x] = game_state.hero
