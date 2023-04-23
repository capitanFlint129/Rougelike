class Gui:
    pass


def echo_level(game_state):
    for row in game_state.level:
        echo(*row, sep="")
        echo("\n")


class ConsoleGui:
    def __init__(self):
        self.old_player_x = None
        self.old_player_y = None
        self.old_enemy_x = None
        self.old_enemy_y = None

    def print_state(self, game_state, term):
        if game_state.level_changed:
            echo(term.home + term.clear)
            echo_level(game_state)
            echo(term.move_yx(game_state.player_y, game_state.player_x) + "O", end="")
            game_state.level_changed = False

        echo_level(game_state)
        echo(term.move_yx(game_state.player_y, game_state.player_x) + "O", end="")
        echo(term.move_yx(game_state.enemy_y, game_state.enemy_x) + "*", end="")
        echo(term.move_yx(24, 10) + str(game_state.score), end="")
        echo(term.move_yx(25, 10) + str(game_state.lives), end="")

        if self.old_player_y is not None and self.old_player_x is not None:
            echo(term.move_yx(self.old_player_y, self.old_player_x) + " ", end="")
        echo(term.move_yx(game_state.player_y, game_state.player_x) + "O", end="")

        if self.old_enemy_y is not None and self.old_enemy_x is not None:
            echo(
                term.move_yx(self.old_enemy_y, self.old_enemy_x)
                + game_state.level[self.old_enemy_y][self.old_enemy_x],
                end="",
            )
        echo(term.move_yx(game_state.enemy_y, game_state.enemy_x) + "*", end="")

        echo(term.move_yx(24, 10) + str(game_state.score), end="")
        echo(term.move_yx(25, 10) + str(game_state.lives), end="")

        self.old_player_x = game_state.player_x
        self.old_player_y = game_state.player_y
        self.old_enemy_x = game_state.enemy_x
        self.old_enemy_y = game_state.enemy_y
