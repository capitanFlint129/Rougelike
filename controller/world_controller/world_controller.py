import state.physical_object as po
from controller.controller import Controller
from events.event_handler import EventHandler
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
            EventHandler.clear_events()
            return

        x, y = game_state.hero.get_x(), game_state.hero.get_y()
        current_cell = game_state.game_map.get_object_at(x, y)

        if game_state.game_map.current_room_is_finale() and isinstance(
            current_cell, po.ExitPortal
        ):
            self.handle_level_completion(game_state)
            EventHandler.clear_events()
        elif isinstance(current_cell, po.Door):
            self.handle_door_transition(game_state, x, y)
            EventHandler.clear_events()
        EventHandler.update()

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

        # TODO: Simplify ?
        player = game_state.hero
        game_map = game_state.game_map

        if x == 0:
            room_direction = "left"
        elif y == 0:
            room_direction = "top"
        elif y == game_map.get_height() - 1:
            room_direction = "bottom"
        else:
            room_direction = "right"

        game_map.change_room(room_direction)

        new_height = game_map.get_height()
        new_width = game_map.get_width()

        if room_direction == "left":
            player_x, player_y = new_width - 3, new_height // 2
        elif room_direction == "top":
            player_x, player_y = new_width // 2, new_height - 3
        elif room_direction == "bottom":
            player_x, player_y = new_width // 2, 3
        else:  # room_direction == "right":
            player_x, player_y = 3, new_height // 2

        if game_map.current_room_is_finale():
            player_x, player_y = 6, 3

        player.move_to(player_x, player_y)
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
        game_state.hero.set_x(game_state.game_map.get_width() // 2)
        game_state.hero.set_y(game_state.game_map.get_height() // 2)
