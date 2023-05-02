import time
from functools import partial

from blessed import Terminal

from controller.controller import Controller
from gui.command_handler import CommandHandler, UserCommand
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
        self.command_handler = command_handler

    def run(self):
        term = Terminal()
        with term.cbreak(), term.fullscreen(), term.hidden_cursor():
            while True:
                if self.command_handler.get_command() == UserCommand.OPEN_INVENTORY:
                    self._open_inventory(term)
                else:
                    self._run_game_step(term)
                if self.state.lives == 0:
                    self._show_game_over_message(term)
                    while self.command_handler.get_command() != UserCommand.APPLY:
                        time.sleep(0.1)
                    exit()

    def _show_game_over_message(self, term):
        echo(term.move_yx(11, 13) + "~" * (37 + len(str(self.state.score))))
        echo(
            term.move_yx(12, 13)
            + f"~Your score is {self.state.score}. Press enter to exit~"
        )
        echo(term.move_yx(13, 13) + "~" * (37 + len(str(self.state.score))))

    def _run_game_step(self, term):
        old_player_coords, old_enemy_coords = self._get_old_coordinates()
        self._apply_controllers()

        if self.state.room_changed:
            old_enemy_coords = {}
            self._handle_room_change(term)

        self._update_display(term, old_player_coords, old_enemy_coords)
        time.sleep(0.1)

    def _open_inventory(self, term):
        user_position = 0
        items_in_menu = 3
        menu_slot_width = 30
        items_list = list(self.state.hero.inventory)
        self._print_inventory(
            term, items_list, user_position, items_in_menu, menu_slot_width
        )
        time.sleep(0.2)
        while True:
            user_command = self.command_handler.get_command()
            if len(items_list) > 0:
                current_item = items_list[user_position]
                if user_command == UserCommand.UP:
                    user_position = max(0, user_position - 1)
                elif user_command == UserCommand.DOWN:
                    user_position = min(len(items_list) - 1, user_position + 1)
                elif user_command == UserCommand.APPLY:
                    if current_item in self.state.hero.equipped:
                        self.state.hero.unequip(current_item)
                    else:
                        self.state.hero.equip(current_item)
            if user_command == UserCommand.OPEN_INVENTORY:
                break
            self._print_inventory(
                term, items_list, user_position, items_in_menu, menu_slot_width
            )
            time.sleep(0.1)
        self._clear_inventory(term, items_in_menu, menu_slot_width)
        time.sleep(0.1)

    def _print_inventory(
        self, term, items_list, user_position, items_in_menu, menu_slot_width
    ):
        self._clear_inventory(term, items_in_menu, menu_slot_width)
        view_start = user_position - user_position % items_in_menu
        view_end = min(view_start + items_in_menu, len(items_list))
        if len(items_list) == 0:
            echo(term.move_yx(24, 39) + "Inventory: 0")
        else:
            echo(term.move_yx(24, 39) + f"Inventory: {view_start + 1}-{view_end}")
        for i in range(0, view_end - view_start):
            current_position = view_start + i
            item_string = self._get_item_string_for_menu(items_list[current_position])[
                :menu_slot_width
            ]
            if current_position == user_position:
                item_string = term.black_on_snow(item_string)
            echo(term.move_yx(25 + i, 39) + item_string)

    def _clear_inventory(self, term, items_in_menu, menu_slot_width):
        for i in range(items_in_menu + 1):
            echo(term.move_yx(24 + i, 39) + " " * menu_slot_width)

    def _get_item_string_for_menu(self, item):
        if item in self.state.hero.equipped:
            return "[x] " + item.get_name()
        return "[ ] " + item.get_name()

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
        echo(
            term.move_yx(self.state.hero.get_y(), self.state.hero.get_x())
            + self.state.hero.get_icon(),
            end="",
        )
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
        health_bar = (
            "["
            + ("|" * num_bars)
            + (" " * num_spaces)
            + "] "
            + str(health_percent)
            + "%"
            + " " * 10
        )
        return health_bar

    @staticmethod
    def _echo_level(game_state):
        for objects in game_state.current_room.game_map:
            for object in objects:
                echo(object.get_icon(), sep="")
            echo("\n")
