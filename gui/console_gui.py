from functools import partial

from blessed import Terminal


class Gui:
    pass


echo = partial(print, end="", flush=True)
echo("")


class ConsoleGui:
    def __init__(self, term: Terminal):
        self.term = term
        self.items_in_menu = 3
        self.menu_slot_width = 30

    def show_game_over_message(self, state):
        echo(self.term.move_yx(11, 13) + "~" * (37 + len(str(state.score))))
        echo(
            self.term.move_yx(12, 13)
            + f"~Your score is {state.score}. Press enter to exit~"
        )
        echo(self.term.move_yx(13, 13) + "~" * (37 + len(str(state.score))))

    def print_inventory(
            self, state, items_list, user_position
    ):
        self.clear_inventory()
        view_start = user_position - user_position % self.items_in_menu
        view_end = min(view_start + self.items_in_menu, len(items_list))
        if len(items_list) == 0:
            echo(self.term.move_yx(24, 39) + "Inventory: 0")
        else:
            echo(self.term.move_yx(24, 39) + f"Inventory: {view_start + 1}-{view_end}")
        for i in range(0, view_end - view_start):
            current_position = view_start + i
            item_string = self.get_item_string_for_menu(state, items_list[current_position])[
                          :self.menu_slot_width
                          ]
            if current_position == user_position:
                item_string = self.term.black_on_snow(item_string)
            echo(self.term.move_yx(25 + i, 39) + item_string)

    def clear_inventory(self):
        for i in range(self.items_in_menu + 1):
            echo(self.term.move_yx(24 + i, 39) + " " * self.menu_slot_width)

    def get_item_string_for_menu(self, state, item):
        if item in state.hero.equipped:
            return "[x] " + item.get_name()
        return "[ ] " + item.get_name()

    def get_old_coordinates(self, state):
        old_player_x, old_player_y = state.hero.get_x(), state.hero.get_y()
        enemies = state.current_room.enemies
        old_enemy_coordinates = [(enemy.get_y(), enemy.get_x()) for enemy in enemies]
        return (old_player_x, old_player_y), old_enemy_coordinates

    def handle_room_change(self, state):
        echo(self.term.home + self.term.clear)
        self._echo_level(state)
        echo(
            self.term.move_yx(state.hero.get_y(), state.hero.get_x())
            + state.hero.get_icon(),
            end="",
        )
        state.room_changed = False

    def update_display(self, state, old_player_coords, old_enemy_coords, max_health):
        old_player_x, old_player_y = old_player_coords
        player_x, player_y = state.hero.get_x(), state.hero.get_y()
        game_map = state.current_room.game_map

        echo(self.term.move_yx(old_player_y, old_player_x) + " ", end="")
        echo(self.term.move_yx(player_y, player_x) + state.hero.get_icon(), end="")

        for (y, x) in old_enemy_coords:
            echo(self.term.move_yx(y, x) + game_map[y][x].get_icon(), end="")
        for enemy in state.current_room.enemies:
            x, y = enemy.get_x(), enemy.get_y()
            echo(self.term.move_yx(y, x) + enemy.get_icon(), end="")

        self.print_status_bar(state, max_health)

    def print_status_bar(self, state, max_health):
        echo(self.term.move_yx(24, 0) + "level: " + str(state.current_level), end="")
        echo(self.term.move_yx(24, 10) + "power: " + str(state.hero.power), end="")
        echo(self.term.move_yx(25, 10) + self._get_health_bar(state, max_health), end="")
        echo(self.term.move_yx(26, 10) + "score: " + str(state.score), end="")
        echo(self.term.move_yx(27, 10) + "lives: " + ("♥" * state.lives), end="")

    @staticmethod
    def _get_health_bar(state, max_health):
        hero_health = state.hero.health
        max_health = max(hero_health, max_health)
        health_percent = int((hero_health / max_health) * 100)
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
