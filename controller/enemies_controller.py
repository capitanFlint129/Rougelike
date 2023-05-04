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
        """
        Updates the position of an enemy in the game by checking if the player is nearby and if not, moves the enemy in
        the direction of the player if possible.

        Args:
            player (Hero): The player character.
            enemy (Enemy): The enemy character.
            game_map (List[List[GameObject]]): The current state of the game map.

        Returns:
            None
        """
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
        """
        Calculates the next coordinates for the enemy to move to in order to get closer to the player.

        Args:
            player_coordinates (Tuple[int, int]): The coordinates of the player.
            enemy_coordinates (Tuple[int, int]): The coordinates of the enemy.

        Returns:
            Tuple[int, int]: The next coordinates for the enemy to move to.
        """

        def sign(x):
            return -1 if x < 0 else (1 if x > 0 else 0)

        dx = sign(player_coordinates.x - enemy_coordinates.x)
        dy = sign(player_coordinates.y - enemy_coordinates.y)

        return enemy_coordinates.x + dx, enemy_coordinates.y + dy

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
