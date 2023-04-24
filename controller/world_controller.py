from controller.controller import Controller
from state.enemy import Enemy
from state.state import State


class WorldController(Controller):
    def update_state(self, game_state: State):
        if not game_state.hero.is_alive:
            exit()
            self.new_level(game_state)
        if (game_state.player_y, game_state.player_x) in game_state.exits_coordinates:
            game_state.current_level += 1
            self.new_level(game_state)

    @staticmethod
    def new_level(game_state):
        game_state.level_changed = True
        enemy_x = 60
        enemy_y = 17
        game_state.player_x = 6
        game_state.player_y = 3
        for row in game_state.level:
            row.clear()
        with open(f"levels/level_{game_state.current_level}.txt", "r") as levels_file:
            game_state.level = [list(line.strip()) for line in levels_file.readlines()]

        enemy = Enemy()
        game_state.enemies.append((enemy_y, enemy_x, enemy, ' '))
        game_state.level[game_state.player_y][game_state.player_x] = game_state.hero
        game_state.level[enemy_y][enemy_x] = enemy

        game_state.level.append(["  Score: ", ""])
        game_state.level.append(["  Lives: ", ""])

        # door
        game_state.exits_coordinates = [(20, 60)]
        game_state.level[20][60] = "+"
