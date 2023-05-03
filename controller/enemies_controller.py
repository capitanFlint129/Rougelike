from controller.controller import Controller
from state.state import State
import state.physical_object as po


class EnemiesController(Controller):
    def update_state(self, game_state: State):
        enemies = game_state.game_map.get_enemies()
        player = game_state.hero
        game_map = game_state.game_map.get_map()

        dead_enemies = set()
        for enemy in enemies:
            if not enemy.is_alive:
                dead_enemies.add(enemy)
            else:
                self._update_enemy_position(player, enemy, game_map)

        self._remove_dead_enemies(enemies, dead_enemies)

    def _update_enemy_position(self, player, enemy, game_map):
        next_x, next_y = self._get_next_coordinates(
            player.coordinates, enemy.coordinates
        )
        next_cell = game_map[next_y][next_x]

        if player.coordinates == (next_x, next_y):
            enemy.attack(player)
        elif not isinstance(next_cell, (po.Wall, po.MapBorder)):
            enemy.move_to(next_x, next_y)

    @staticmethod
    def _get_next_coordinates(player_coordinates, enemy_coordinates):
        def sign(x):
            return -1 if x < 0 else (1 if x > 0 else 0)

        dx = sign(player_coordinates.x - enemy_coordinates.x)
        dy = sign(player_coordinates.y - enemy_coordinates.y)

        return enemy_coordinates.x + dx, enemy_coordinates.y + dy

    @staticmethod
    def _remove_dead_enemies(enemies, dead_enemies):
        for dead_enemy in dead_enemies:
            enemies.discard(dead_enemy)
