from controller.controller import Controller
from controller.world_controller import new_level
from gui.command_handler import CommandHandler, UserCommand
from state.state import State





class PlayerController(Controller):
    def __init__(self, command_handler: CommandHandler):
        self.command_handler = command_handler

    def update_state(self, game_state: State):
        move_up = True
        move_down = True
        move_right = True
        move_left = True
        game_state.last_x = game_state.player_x
        game_state.last_y = game_state.player_y
        y_up = game_state.level[game_state.player_y + 1][game_state.player_x]
        y_down = game_state.level[game_state.player_y - 1][game_state.player_x]
        x_right = game_state.level[game_state.player_y][game_state.player_x + 1]
        x_left = game_state.level[game_state.player_y][game_state.player_x - 1]
        if y_up == "#":
            move_up = False
        if y_down == "#":
            move_down = False
        if x_right == "#":
            move_right = False
        if x_left == "#":
            move_left = False

        if move_down == True:
            if self.command_handler.get_command() == UserCommand.UP:
                game_state.player_y = game_state.player_y - 1
                if y_down == "^" or y_down == ">" or y_down == "v" or y_down == "<":
                    game_state.score = 0
                    game_state.lives -= 1
                    new_level(game_state)
                if y_down == "c":
                    game_state.score += 1
                if y_down == "H":
                    game_state.lives += 1
        if move_up == True:
            if self.command_handler.get_command() == UserCommand.DOWN:
                game_state.player_y = game_state.player_y + 1
                if y_up == "^" or y_up == ">" or y_up == "v" or y_up == "<":
                    game_state.score = 0
                    game_state.lives -= 1
                    new_level(game_state)
                if y_up == "c":
                    game_state.score += 1
                if y_up == "H":
                    game_state.lives += 1
        if move_left == True:
            if self.command_handler.get_command() == UserCommand.LEFT:
                game_state.player_x = game_state.player_x - 1
                if x_left == "^" or x_left == ">" or x_left == "v" or x_left == "<":
                    game_state.score = 0
                    game_state.lives -= 1
                    new_level(game_state)
                if x_left == "c":
                    game_state.score += 1
                if x_left == "H":
                    game_state.lives += 1
        if move_right == True:
            if self.command_handler.get_command() == UserCommand.RIGHT:
                game_state.player_x = game_state.player_x + 1
                if x_right == "^" or x_right == ">" or x_right == "v" or x_right == "<":
                    game_state.score = 0
                    game_state.lives -= 1
                    new_level(game_state)
                if x_right == "c":
                    game_state.score += 1
                if x_right == "H":
                    game_state.lives += 1
