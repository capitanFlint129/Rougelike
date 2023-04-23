from controller.enemies_controller import EnemiesController
from controller.player_controller import PlayerController
from controller.player_controller import new_level
from controller.world_controller import WorldController
from game_engine.game_engine import GameEngine
from gui.command_handler import CommandHandler
from state.state import State

if __name__ == "__main__":
    game_state = State()
    commands_handler = CommandHandler()
    player_controller = PlayerController(commands_handler)
    enemies_controller = EnemiesController()
    world_controller = WorldController()
    game_engine = GameEngine(
        game_state,
        [player_controller, enemies_controller, world_controller],
        commands_handler,
    )
    new_level(game_state)
    game_engine.run()
