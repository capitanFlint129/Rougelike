from state.state import State
from controller.controller import Controller


class EnemiesController(Controller):
    def update_state(self, game_state: State):
        e_move_up = True
        e_move_down = True
        e_move_right = True
        e_move_left = True

        game_state.e_last_x = game_state.enemy_x
        game_state.e_last_y = game_state.enemy_y
        y_up = game_state.level[game_state.enemy_y + 1][game_state.enemy_x]
        y_down = game_state.level[game_state.enemy_y - 1][game_state.enemy_x]
        x_right = game_state.level[game_state.enemy_y][game_state.enemy_x + 1]
        x_left = game_state.level[game_state.enemy_y][game_state.enemy_x - 1]
        if y_up == "#" or y_up == "^" or y_up == ">" or y_up == "<" or y_up == "v":
            e_move_up = False
        if y_down == "#" or y_down == "^" or y_down == ">" or y_down == "<" or y_down == "v":
            e_move_down = False
        if x_right == "#" or x_right == "^" or x_right == ">" or x_right == "<" or x_right == "v":
            e_move_right = False
        if x_left == "#" or x_left == "^" or x_left == ">" or x_left == "<" or x_left == "v":
            e_move_left = False

        if e_move_up == True and game_state.player_y > game_state.enemy_y:
            game_state.enemy_y += 1
        if e_move_down == True and game_state.player_y < game_state.enemy_y:
            game_state.enemy_y -= 1
        if e_move_right == True and game_state.player_x > game_state.enemy_x:
            game_state.enemy_x += 1
        if e_move_left == True and game_state.player_x < game_state.enemy_x:
            game_state.enemy_x -= 1
