import state.physical_object as po
from controller.controller import Controller
from generators.map_generator import MapGenerator
from state.state import State


class WorldController(Controller):
    """
    Controller for handling the game world state.
    """

    def update_state(self, game_state: State):
        """
        Updates the game state and the current game map based on the current state of the game.

        Args:
            game_state (State): The current state of the game.
        """
        if not game_state.hero.is_alive:
            game_state.lives -= 1
            game_state.hero.resurrect_player()
            self.new_level(game_state)
            return

        x, y = game_state.hero.get_x(), game_state.hero.get_y()
        current_cell = game_state.game_map.get_object_at(x, y)

        if game_state.game_map.current_room_is_finale() and isinstance(
            current_cell, po.ExitPortal
        ):
            self.handle_level_completion(game_state)
        elif isinstance(current_cell, po.Door):
            self.handle_door_transition(game_state, x, y)

    def handle_level_completion(self, game_state):
        """
        Handles the completion of a level, updates the game state and sets the hero's new location.

        Args:
            game_state (State): The current state of the game.
        """
        game_state.current_level += 1
        game_state.hero.move_to(5, 5)
        self.new_level(game_state)

    @staticmethod
    def handle_door_transition(game_state, x, y):
        """
        Handles a door transition, changing the current game map and hero's location based on the location of the door.

        Args:
            game_state (State): The current state of the game.
            x (int): The x-coordinate of the door.
            y (int): The y-coordinate of the door.
        """
        height = game_state.game_map.get_height()
        width = game_state.game_map.get_width()
        player = game_state.hero
        game_map = game_state.game_map
        if x == 0:
            game_map.change_room("left")
            player.move_to(width - 3, player.get_y())
        elif y == 0:
            game_map.change_room("top")
            player.move_to(player.get_x(), height - 3)
        elif y == height - 1:
            game_map.change_room("bottom")
            player.move_to(player.get_x(), 3)
        else:
            game_map.change_room("right")
            player.move_to(3, player.get_y())

        if game_map.current_room_is_finale():
            player.move_to(6, 3)

        game_state.room_changed = True

    @staticmethod
    def new_level(game_state):
        """
        Generates a new level for the game.

        Args:
            game_state (State): The current state of the game.
        """
        game_state.room_changed = True
        game_state.game_map = MapGenerator.generate_new_map(game_state.current_level)
        game_state.hero.set_x(game_state.game_map.get_height() // 2)
        game_state.hero.set_y(game_state.game_map.get_width() // 2)
