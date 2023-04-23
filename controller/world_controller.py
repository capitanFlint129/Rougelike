import time
from functools import partial

from controller.player_controller import new_level
from state.state import State

echo = partial(print, end='', flush=True)
echo('')


class WorldController:
    def update_state(self, game_state: State):
        if game_state.player_x == game_state.enemy_x and game_state.player_y == game_state.enemy_y:
            game_state.score = 0
            game_state.lives -= 1
            new_level(game_state)
        if game_state.lives == 0:
            echo("You Win!")
            time.sleep(1)
            play_again = input("press enter to replay")
            if play_again == '':
                game_state.current_level = 0
                game_state.score = 0
                game_state.lives = 5
                new_level(game_state)
            else:
                time.sleep(1)
                echo("thank you for playing")
                time.sleep(1)
                exit()
        if game_state.level[game_state.player_y][game_state.player_x] == '+':
            game_state.current_level += 1
            if game_state.current_level == 9:
                echo("You Lose!")
                time.sleep(1)
                play_again = input('press enter to replay')
                if play_again == '':
                    game_state.current_level = 0
                    new_level(game_state)
                else:
                    time.sleep(1)
                    echo("thank you for playing")
                    time.sleep(1)
                    exit()
            new_level(game_state)
