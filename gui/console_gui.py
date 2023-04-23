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
        self.old_enemy_coordinates = []

    def print_state(self, game_state, term):
        if game_state.level_changed:
            echo(term.home + term.clear)
            echo_level(game_state)
            echo(term.move_yx(game_state.player_y, game_state.player_x) + "O", end="")
            game_state.level_changed = False

        echo_level(game_state)
        echo(term.move_yx(game_state.player_y, game_state.player_x) + "O", end="")
        for enemy_x, enemy_y, enemy, _ in game_state.enemies:
            echo(term.move_yx(enemy_y, enemy_x) + enemy.get_icon(), end="")
        echo(term.move_yx(24, 10) + str(game_state.score), end="")
        echo(term.move_yx(25, 10) + str(game_state.lives), end="")

        if self.old_player_y is not None and self.old_player_x is not None:
            echo(term.move_yx(self.old_player_y, self.old_player_x) + " ", end="")
        echo(term.move_yx(game_state.player_y, game_state.player_x) + "O", end="")

        for y, x in self.old_enemy_coordinates:
            echo(term.move_yx(y, x) + game_state.level[y][x], end="")
        echo(term.move_yx(game_state.enemy_y, game_state.enemy_x) + "*", end="")

        echo(term.move_yx(24, 10) + str(game_state.score), end="")
        echo(term.move_yx(25, 10) + str(game_state.lives), end="")

        self.old_player_x = game_state.player_x
        self.old_player_y = game_state.player_y
        self.old_enemy_coordinates = [(y, x) for y, x, _, _ in game_state.enemies]
