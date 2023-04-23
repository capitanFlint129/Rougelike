from controller.controller import Controller
from state.state import State


class EnemiesController(Controller):
    def update_state(self, game_state: State):
        game_state.e_last_x = game_state.enemy_x
        game_state.e_last_y = game_state.enemy_y

        next_y = game_state.enemy_y
        next_x = game_state.enemy_x
        if game_state.player_y > game_state.enemy_y:
            next_y += 1
        if game_state.player_y < game_state.enemy_y:
            next_y -= 1
        if game_state.player_x > game_state.enemy_x:
            next_x += 1
        if game_state.player_x < game_state.enemy_x:
            next_x -= 1

        next_cell = game_state.level[next_y][next_x]

        if next_cell not in ["#", "^", ">", "<", "v"]:
            game_state.enemy_y = next_y
            game_state.enemy_x = next_x
