from blessed import Terminal

from controller import EnemiesController, PlayerController, WorldController
from game_engine.game_engine import GameEngine
from game_engine.inventory_menu.inventory_menu import InventoryMenu
from gui.command_handler import (
    PlayerControllerCommandHandler,
    GameEngineCommandHandler,
    InventoryMenuCommandHandler,
)
from gui.console_gui import ConsoleGUI
from state.hero import Hero
from state.state import State

if __name__ == "__main__":
    term = Terminal()
    with term.cbreak(), term.fullscreen(), term.hidden_cursor():
        hero = Hero()
        game_state = State(hero)
        gui = ConsoleGUI(term)
        inventory_menu_command_handler = InventoryMenuCommandHandler()
        inventory_menu = InventoryMenu(game_state, gui, inventory_menu_command_handler)
        player_controller_command_handler = PlayerControllerCommandHandler()
        game_engine_command_handler = GameEngineCommandHandler(inventory_menu)

        player_controller = PlayerController(player_controller_command_handler)
        enemies_controller = EnemiesController()
        world_controller = WorldController()
        game_engine = GameEngine(
            game_state,
            [player_controller, enemies_controller, world_controller],
            game_engine_command_handler,
            gui,
        )
        world_controller.new_level(game_state)
        game_engine.run()
