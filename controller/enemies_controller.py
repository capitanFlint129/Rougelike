import state.physical_object as po
from controller.controller import Controller
from state.state import State


class EnemiesController(Controller):
    """
    A controller that updates the state of enemies in the game by checking their positions relative to the player and
    the environment and making any necessary updates to their position or attacking the player.

    Args:
        Controller (class): A base class for controllers that updates the game state.
    """

    def update_state(self, game_state: State):
        """
        Updates the game state by moving the enemies in the game.

        Args:
            game_state (State): The current state of the game.

        Returns:
            None
        """
        enemies = game_state.game_map.get_enemies()

        dead_enemies = set()
        for enemy in enemies:
            if not enemy.is_alive:
                dead_enemies.add(enemy)
            else:
                self._update_enemy_position(enemy, game_state)

        self._remove_dead_enemies(enemies, dead_enemies)

    def _update_enemy_position(self, enemy, game_state: State):
        """
        Updates the position of an enemy in the game by checking if the player is nearby and if not, moves the enemy in
        the direction of the player if possible.

        Args:
            enemy (Enemy): The enemy character.
            game_state (State): The current state of the game.

        Returns:
            None
        """
        game_map = game_state.game_map.get_map()
        player = game_state.hero
        next_x, next_y = enemy.move(game_state)
        next_cell = game_map[next_y][next_x]

        if player.coordinates == (next_x, next_y):
            enemy.attack(player)
        elif not isinstance(next_cell, (po.Wall, po.MapBorder)):
            enemy.move_to(next_x, next_y)

    @staticmethod
    def _remove_dead_enemies(enemies, dead_enemies):
        """
        Removes dead enemies from the set of enemies in the game.

        Args:
            enemies (Set[Enemy]): The current set of enemies in the game.
            dead_enemies (Set[Enemy]): The set of dead enemies.

        Returns:
            None
        """
        for dead_enemy in dead_enemies:
            enemies.discard(dead_enemy)
