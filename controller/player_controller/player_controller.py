from controller.controller import Controller
from gui.command_handler import PlayerControllerCommandHandler
from state.state import State


class PlayerController(Controller):
    """
    This class represents the controller for the player character in the game.
    It handles the player's movements and interactions with the game objects.
    """

    def __init__(self, command_handler: PlayerControllerCommandHandler):
        self.command_handler = command_handler

    def update_state(self, game_state: State):
        """
        Updates the game state based on the player's actions.

        Args:
            game_state (State): The current state of the game.

        Return:
            None
        """
        command = self.command_handler.get_command()
        if command is not None:
            command.execute(game_state)
