import time
from functools import partial

from controller.controller import Controller
from state.state import State

echo = partial(print, end='', flush=True)
echo('')


def clear_level(game_state):
    for row in game_state.level:
        row.clear()


class WorldController(Controller):
    def update_state(self, game_state: State):
        if game_state.player_x == game_state.enemy_x and game_state.player_y == game_state.enemy_y:
            game_state.score = 0
            game_state.lives -= 1
            self.new_level(game_state)
        if game_state.lives == 0:
            echo("You Lose!")
            time.sleep(1)
            play_again = input("press enter to replay")
            if play_again == '':
                game_state.current_level = 0
                game_state.score = 0
                game_state.lives = 5
                self.new_level(game_state)
            else:
                time.sleep(1)
                echo("thank you for playing")
                time.sleep(1)
                exit()
            self.new_level(game_state)
        if game_state.level[game_state.player_y][game_state.player_x] == '+':
            game_state.current_level += 1
            self.new_level(game_state)

    @staticmethod
    def new_level(game_state):
        game_state.level_changed = True
        game_state.enemy_x = 60
        game_state.enemy_y = 17
        game_state.player_x = 6
        game_state.player_y = 3
        clear_level(game_state)
        with open(f'levels/level_{game_state.current_level}.txt', 'r') as levels_file:
            game_state.level = [list(line.strip()) for line in levels_file.readlines()]

        game_state.level.append(["  Score: ", ""])
        game_state.level.append(["  Lives: ", ""])

        # door
        game_state.level[20][60] = '+'
