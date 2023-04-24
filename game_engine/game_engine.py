import time
from functools import partial

from blessed import Terminal

from controller.controller import Controller
from gui.command_handler import CommandHandler
from state.state import State

echo = partial(print, end="", flush=True)
echo("")


class GameEngine:
    def __init__(
        self,
        state: State,
        controllers: [Controller],
        command_handler: CommandHandler,
    ):
        self.state = state
        self.controllers = controllers

    def run(self):
        term = Terminal()
        with term.cbreak(), term.fullscreen(), term.hidden_cursor():
            while True:
                if self.state.level_changed:
                    echo(term.home + term.clear)
                    self._echo_level(self.state)
                    echo(
                        term.move_yx(self.state.player_y, self.state.player_x)
                        + self.state.hero.get_icon(),
                        end="",
                    )
                    self.state.level_changed = False

                old_player_x = self.state.player_x
                old_player_y = self.state.player_y
                old_enemy_coordinates = [(y, x) for y, x, _, _ in self.state.enemies]

                self._apply_controllers()

                echo(term.move_yx(old_player_y, old_player_x) + " ", end="")
                echo(
                    term.move_yx(self.state.player_y, self.state.player_x)
                    + self.state.hero.get_icon(),
                    end="",
                )

                for y, x in old_enemy_coordinates:
                    echo(term.move_yx(y, x) + str(self.state.level[y][x]), end="")
                for y, x, enemy, _ in self.state.enemies:
                    echo(term.move_yx(y, x) + enemy.get_icon(), end="")

                echo(term.move_yx(24, 10) + str(self.state.score), end="")
                echo(term.move_yx(25, 10) + str(self.state.hero.health), end="")

                time.sleep(0.1)

    def _apply_controllers(self):
        for controller in self.controllers:
            controller.update_state(self.state)

    @staticmethod
    def _echo_level(game_state):
        for row in game_state.level:
            echo(*row, sep="")
            echo("\n")
