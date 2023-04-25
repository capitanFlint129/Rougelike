from controller.controller import Controller
from state.hero import Hero
from state.state import State
import state.physical_object as po


class EnemiesController(Controller):

    def update_state(self, game_state: State):
        enemies = game_state.current_room.enemies
        player = game_state.hero
        game_map = game_state.current_room.game_map
        for enemy in enemies:
            if not enemy.is_alive:
                enemies.discard(enemy)
                continue
            enemy_x, enemy_y = enemy.coordinates.x, enemy.coordinates.y
            next_x, next_y = enemy_x, enemy_y
            player_x, player_y = player.coordinates.x, player.coordinates.y
            if player_y > next_y:
                next_y += 1
            if player_y < enemy_y:
                next_y -= 1
            if player_x > enemy_x:
                next_x += 1
            if player_x < enemy_x:
                next_x -= 1

            next_cell = game_map[next_y][next_x]

            if player_x == next_x and player_y == next_y:
                enemy.attack(player)
                continue
            if isinstance(next_cell, po.Wall) or isinstance(next_cell, po.MapBorder):
                continue
            enemy.move_to(next_x, next_y)
