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
        self.max_health = 0

    def run(self):
        term = Terminal()
        with term.cbreak(), term.fullscreen(), term.hidden_cursor():
            while True:
                old_player_coords, old_enemy_coords = self._get_old_coordinates()
                self._apply_controllers()

                if self.state.room_changed:
                    old_enemy_coords = {}
                    self._handle_room_change(term)

                self._update_display(term, old_player_coords, old_enemy_coords)
                time.sleep(0.1)

    def _apply_controllers(self):
        for controller in self.controllers:
            controller.update_state(self.state)

    def _get_old_coordinates(self):
        old_player_x, old_player_y = self.state.hero.get_x(), self.state.hero.get_y()
        enemies = self.state.current_room.enemies
        old_enemy_coordinates = [(enemy.get_y(), enemy.get_x()) for enemy in enemies]
        return (old_player_x, old_player_y), old_enemy_coordinates

    def _handle_room_change(self, term):
        echo(term.home + term.clear)
        self._echo_level(self.state)
        echo(term.move_yx(self.state.hero.get_y(), self.state.hero.get_x()) + self.state.hero.get_icon(), end="")
        self.state.room_changed = False

    def _update_display(self, term, old_player_coords, old_enemy_coords):
        old_player_x, old_player_y = old_player_coords
        player_x, player_y = self.state.hero.get_x(), self.state.hero.get_y()
        game_map = self.state.current_room.game_map

        echo(term.move_yx(old_player_y, old_player_x) + " ", end="")
        echo(term.move_yx(player_y, player_x) + self.state.hero.get_icon(), end="")

        for (y, x) in old_enemy_coords:
            echo(term.move_yx(y, x) + game_map[y][x].get_icon(), end="")
        for enemy in self.state.current_room.enemies:
            x, y = enemy.get_x(), enemy.get_y()
            echo(term.move_yx(y, x) + enemy.get_icon(), end="")

        self._print_status_bar(term)

    def _print_status_bar(self, term):
        echo(term.move_yx(24, 0) + "level: " + str(self.state.current_level), end="")
        echo(term.move_yx(24, 10) + "power: " + str(self.state.hero.power), end="")
        echo(term.move_yx(25, 10) + self._get_health_bar(), end="")
        echo(term.move_yx(26, 10) + "score: " + str(self.state.score), end="")
        echo(term.move_yx(27, 10) + "lives: " + ("♥" * self.state.lives), end="")

    def _get_health_bar(self):
        hero_health = self.state.hero.health
        self.max_health = max(hero_health, self.max_health)
        health_percent = int((hero_health / self.max_health) * 100)
        num_bars = int(health_percent / 10)
        num_spaces = 10 - num_bars
        health_bar = "[" + ("|" * num_bars) + (" " * num_spaces) + "] " + str(health_percent) + "%" + " " * 10
        return health_bar

    @staticmethod
    def _echo_level(game_state):
        for objects in game_state.current_room.game_map:
            for object in objects:
                echo(object.get_icon(), sep="")
            echo("\n")
