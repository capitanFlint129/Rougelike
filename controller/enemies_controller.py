from controller.controller import Controller
from state.hero import Hero
from state.state import State


class EnemiesController(Controller):
    def update_state(self, game_state: State):
        new_enemies = []
        for enemy_y, enemy_x, enemy, previous_item in game_state.enemies:
            game_state.level[enemy_y][enemy_x] = previous_item
            if not enemy.is_alive:
                continue
            next_y = enemy_y
            next_x = enemy_x
            if game_state.player_y > enemy_y:
                next_y += 1
            if game_state.player_y < enemy_y:
                next_y -= 1
            if game_state.player_x > enemy_x:
                next_x += 1
            if game_state.player_x < enemy_x:
                next_x -= 1

            next_cell = game_state.level[next_y][next_x]

            if isinstance(next_cell, Hero):
                game_state.hero.attack(next_cell)
            elif next_cell not in ["#", "^", ">", "<", "v"]:
                if (enemy_y, enemy_x) != (next_y, next_x):
                    previous_item = game_state.level[next_y][next_x]
                enemy_y = next_y
                enemy_x = next_x
            game_state.level[enemy_y][enemy_x] = enemy
            new_enemies.append((enemy_y, enemy_x, enemy, previous_item))
        game_state.enemies = new_enemies
