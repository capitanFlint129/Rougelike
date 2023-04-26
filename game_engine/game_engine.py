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
                old_player_x, old_player_y = (
                    self.state.hero.get_x(),
                    self.state.hero.get_y(),
                )

                enemies = self.state.current_room.enemies
                old_enemy_coordinates = [
                    (enemy.get_y(), enemy.get_x()) for enemy in enemies
                ]
                self._apply_controllers()
                if self.state.room_changed:
                    old_enemy_coordinates = {}
                    echo(term.home + term.clear)
                    self._echo_level(self.state)
                    echo(
                        term.move_yx(old_player_y, old_player_x)
                        + self.state.hero.get_icon(),
                        end="",
                    )
                    self.state.room_changed = False

                player_x, player_y = self.state.hero.get_x(), self.state.hero.get_y()

                echo(term.move_yx(old_player_y, old_player_x) + " ", end="")
                echo(
                    term.move_yx(player_y, player_x) + self.state.hero.get_icon(),
                    end="",
                )
                game_map = self.state.current_room.game_map
                for (y, x) in old_enemy_coordinates:
                    echo(term.move_yx(y, x) + game_map[y][x].get_icon(), end="")
                for enemy in enemies:
                    x, y = enemy.get_x(), enemy.get_y()
                    echo(term.move_yx(y, x) + enemy.get_icon(), end="")

                echo(term.move_yx(24, 10) + str(self.state.score), end="")
                echo(term.move_yx(25, 10) + str(self.state.lives), end="")

                time.sleep(0.1)

    def _apply_controllers(self):
        for controller in self.controllers:
            controller.update_state(self.state)

    @staticmethod
    def _echo_level(game_state):
        for objects in game_state.current_room.game_map:
            for object in objects:
                echo(object.get_icon(), sep="")
            echo("\n")
