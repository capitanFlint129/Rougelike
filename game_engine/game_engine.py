import time
from functools import partial

from controller.controller import Controller
from gui.command_handler import CommandHandler, UserCommand
from gui.console_gui import ConsoleGUI
from state.state import State
from game_engine.inventory_menu import InventoryMenu

echo = partial(print, end="", flush=True)
echo("")


class GameEngine:
    """
    Runs the main game loop that updates the game state, applies controllers and displays the game on the console.
    """

    def __init__(
        self,
        state: State,
        controllers: [Controller],
        command_handler: CommandHandler,
        gui: ConsoleGUI,
    ):
        """
        Initializes the GameEngine instance.

        Args:
            state: The initial game state.
            controllers: The list of controllers that update the game state.
            command_handler: The handler that maps user keyboard input to game commands.
            gui: The console GUI that displays the game state on the console.
        """
        self.state = state
        self.controllers = controllers
        self.max_health = self.state.hero.health
        self.command_handler = command_handler
        self.gui = gui
        self.inventory_menu = InventoryMenu(self.state, self.gui, self.command_handler)

    def run(self):
        """
        Runs the main game loop that updates the game state, applies controllers and displays the game on the console.
        """
        while True:
            if self.command_handler.get_command() == UserCommand.OPEN_INVENTORY:
                self.inventory_menu.open()
            else:
                self._run_game_step()
            if self.state.lives == 0:
                self.gui.show_game_over_message(self.state.score)
                while self.command_handler.get_command() != UserCommand.APPLY:
                    time.sleep(0.1)
                return

    def _run_game_step(self):
        """
        Runs one step of the game loop, which updates the game state and displays it on the console.
        """
        old_player_coords, old_enemy_coords = self._get_old_coordinates()
        self._apply_controllers()

        if self.state.room_changed:
            old_enemy_coords = {}
            self.gui.handle_room_change(self.state)

        self.gui.update_display(
            self.state, old_player_coords, old_enemy_coords, self.max_health
        )
        time.sleep(0.1)

    def _apply_controllers(self):
        """
        Updates the game state using the registered controllers.
        """
        for controller in self.controllers:
            controller.update_state(self.state)

    def _get_old_coordinates(self):
        """
        Returns the old player and enemy coordinates.

        Returns:
            A tuple containing the old player coordinates and a list of old enemy coordinates.
        """
        old_player_x, old_player_y = self.state.hero.get_x(), self.state.hero.get_y()
        enemies = self.state.game_map.get_enemies()
        old_enemy_coordinates = [(enemy.get_y(), enemy.get_x()) for enemy in enemies]
        return (old_player_x, old_player_y), old_enemy_coordinates