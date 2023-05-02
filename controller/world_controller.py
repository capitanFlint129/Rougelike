import time

from controller.controller import Controller
from state.state import State
from generators.map_generator import MapGenerator
import state.physical_object as po


class WorldController(Controller):
    def update_state(self, game_state: State):
        if game_state.lives == 0:
            self.handle_game_over(game_state)
            return
        if not game_state.hero.is_alive:
            game_state.lives -= 1
            game_state.hero.resurrect_player()
            self.new_level(game_state)
            return

        x, y = game_state.hero.get_x(), game_state.hero.get_y()
        game_map = game_state.current_room.game_map

        if game_state.current_room.is_finale and isinstance(game_map[y][x], po.ExitPortal):
            self.handle_level_completion(game_state)
        elif isinstance(game_map[y][x], po.Door):
            self.handle_door_transition(game_state, x, y)

    def handle_game_over(self, game_state):
        time.sleep(1)
        play_again = input("press enter to replay")
        if play_again == "":
            self.reset_game(game_state)
        else:
            time.sleep(1)
            exit()

    def reset_game(self, game_state):
        game_state.current_level = 0
        game_state.score = 0
        game_state.lives = 5
        self.new_level(game_state)

    def handle_level_completion(self, game_state):
        game_state.current_level += 1
        game_state.hero.move_to(5, 5)
        self.new_level(game_state)

    @staticmethod
    def handle_door_transition(game_state, x, y):
        height = game_state.current_room.height
        width = game_state.current_room.width
        player = game_state.hero

        if x == 0:
            game_state.current_room = game_state.current_room.left
            player.move_to(width - 3, player.get_y())
        elif y == 0:
            game_state.current_room = game_state.current_room.top
            player.move_to(player.get_x(), height - 3)
        elif y == height - 1:
            game_state.current_room = game_state.current_room.bottom
            player.move_to(player.get_x(), 3)
        else:
            game_state.current_room = game_state.current_room.right
            player.move_to(3, player.get_y())

        if game_state.current_room.is_finale:
            player.move_to(6, 3)

        game_state.room_changed = True

    @staticmethod
    def new_level(game_state):
        game_state.room_changed = True
        game_state.current_room = MapGenerator(game_state.current_level).generate_new_map()
        game_state.hero.set_x(game_state.current_room.height // 2)
        game_state.hero.set_y(game_state.current_room.width // 2)
