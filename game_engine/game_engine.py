import time
from functools import partial

from controller.controller import Controller
from gui.command_handler import CommandHandler, UserCommand
from gui.console_gui import ConsoleGui
from state.state import State

echo = partial(print, end="", flush=True)
echo("")


class GameEngine:
    def __init__(
        self,
        state: State,
        controllers: [Controller],
        command_handler: CommandHandler,
        gui: ConsoleGui,
    ):
        self.state = state
        self.controllers = controllers
        self.max_health = self.state.hero.health
        self.command_handler = command_handler
        self.gui = gui

    def run(self):
        while True:
            if self.command_handler.get_command() == UserCommand.OPEN_INVENTORY:
                self._open_inventory()
            else:
                self._run_game_step()
            if self.state.lives == 0:
                self.gui.show_game_over_message(self.state)
                while self.command_handler.get_command() != UserCommand.APPLY:
                    time.sleep(0.1)
                return

    def _run_game_step(self):
        old_player_coords, old_enemy_coords = self._get_old_coordinates()
        self._apply_controllers()

        if self.state.room_changed:
            old_enemy_coords = {}
            self.gui.handle_room_change(self.state)

        self.gui.update_display(
            self.state, old_player_coords, old_enemy_coords, self.max_health
        )
        time.sleep(0.1)

    def _open_inventory(self):
        user_position = 0
        items_list = list(self.state.hero.inventory)
        self.gui.print_inventory(self.state, items_list, user_position)
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
            if user_command is not None:
                self.gui.print_inventory(self.state, items_list, user_position)
            time.sleep(0.1)
        self.gui.clear_inventory()
        time.sleep(0.1)

    def _apply_controllers(self):
        for controller in self.controllers:
            controller.update_state(self.state)

    def _get_old_coordinates(self):
        old_player_x, old_player_y = self.state.hero.get_x(), self.state.hero.get_y()
        enemies = self.state.game_map.get_enemies()
        old_enemy_coordinates = [(enemy.get_y(), enemy.get_x()) for enemy in enemies]
        return (old_player_x, old_player_y), old_enemy_coordinates
