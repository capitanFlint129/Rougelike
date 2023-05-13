import random
from abc import ABC, abstractmethod
from state.actor import Actor
from state.item import Item
from utils.coordinates import Coordinates
import state.enemy_state as es
import copy


class Enemy(Actor):
    """
    Represents an enemy character within a game. Inherits from the Actor class, and overrides the "get_icon" and
    "get_name" methods to provide the enemy's visual representation and name. The class also overrides the "equip" and
    "get_item" methods to prevent the enemy from equipping or picking up items.
    """

    def __init__(self, x=60, y=17):
        super(Enemy, self).__init__(x, y)
        self.wounded_level = self.health // 3
        self.movement = es.EnemyMovement()
        self.original_strategy = None
        self.wounded = False
        self.wounded_strategy = es.CowardlyEnemyState()
        self.regeneration = 1

    def get_icon(self):
        return "*"

    def get_name(self):
        return "enemy"

    def equip(self, item: Item):
        pass

    def get_damage(self, damage):
        super().get_damage(damage)
        if self.health <= self.wounded_level:
            self.wounded = True
            self.original_strategy = self.movement.state
            self.movement.set_state(self.wounded_strategy)

    def get_item(self, item: Item):
        pass

    def enemy_experience(self) -> int:
        pass

    def update(self, game_state) -> Coordinates:
        self._heal()
        player_coordinates = game_state.hero.coordinates
        return self.movement.move(self.coordinates, player_coordinates)

    def _heal(self):
        if self.wounded:
            self.health += self.regeneration
            if self.health > self.wounded_level:
                self.movement.set_state(self.original_strategy)


class CloneableEnemy(Enemy):
    """
    Represents an enemy character that can clone itself with a certain probability.
    Inherits from the Enemy class, and overrides the "update" method to implement the cloning behavior.
    """

    def __init__(self, x, y):
        super().__init__(x, y)
        self.cloning_probability = 0.5

    def clone(self, coordinates=None):
        """
        Clones the enemy and returns a new instance with the same state as the original, but at the given coordinates.
        If no coordinates are given, the clone will appear at the original enemy's location.

        :param coordinates: The coordinates where the clone will appear. Defaults to the original enemy's location.
        :return: A new CloneableEnemy instance with the same state as the original.
        """
        if coordinates is None:
            coordinates = self.coordinates
        new_enemy = copy.deepcopy(self)
        new_enemy.coordinates = coordinates
        return new_enemy

    def update(self, game_state) -> Coordinates:
        """
        Updates the state of the enemy for the current game state, and returns its new coordinates.

        If the enemy's cloning probability is high enough, it will create a new clone at a random adjacent position
        on the game map, with half the original probability of cloning.

        :param game_state: The current game state.
        :return: The new coordinates of the enemy after the update.
        """
        new_coordinates = super().update(game_state)
        if random.random() < self.cloning_probability:
            x, y = self.coordinates
            available_position = []
            game_map = game_state.game_map
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if i == j == 0:
                        continue
                    if game_map.get_object_at(x + i, y + j).get_icon() == " ":
                        available_position.append(Coordinates(x + i, y + j))
            if available_position:
                self.cloning_probability = self.cloning_probability * 0.5
                enemy_copy = self.clone(
                    available_position[random.randint(0, len(available_position)) - 1]
                )
                game_map.set_object_at(
                    *available_position[random.randint(0, len(available_position)) - 1],
                    enemy_copy
                )
                game_map.get_enemies().add(enemy_copy)
        return new_coordinates


"""
Fantasy Enemies:
"""


class Dragon(Enemy):
    """
    Dragon: A massive, fire-breathing beast with impenetrable scales and deadly talons.
    It aggressively pursues its prey, exhibiting immense strength and power.
    """

    def __init__(self, x=60, y=17):
        super().__init__(x, y)
        self.movement.set_state(es.AggressiveEnemyState())

    def get_icon(self):
        return "D"

    def get_name(self):
        return "Dragon"

    def enemy_experience(self) -> int:
        return 2


class ShieldspikeTurtles(Enemy):
    """
    Shieldspike Turtles:
    These large, heavily armored turtles are equipped with sharp spikes protruding from their shells.
    They remain stationary, adopting a defensive posture when threatened.
    When attacked, they quickly retract their limbs and head, using their spiked shell to deflect incoming blows
    and counterattack by spinning rapidly to damage their foes.
    """

    def __init__(self, x=60, y=17):
        super().__init__(x, y)
        self.movement_strategy.set_strategy(es.PassiveEnemyStrategy())

    def get_icon(self):
        return "S"

    def get_name(self):
        return "Skeleton"

    def enemy_experience(self) -> int:
        return 1


class DemonSword(Enemy):
    """
    Looks like sword but has surprise
    """

    def __init__(self, x=60, y=17):
        super().__init__(x, y)
        self.power = 100
        self.movement.set_state(es.PassiveAttackEnemyState())

    def get_icon(self):
        return "|"

    def get_name(self):
        return "Demon Sword"

    def enemy_experience(self) -> int:
        return 1


class PanicPuffs(Enemy):
    """
    Panic Puffs: These round, fluffy creatures are reminiscent of cotton balls and are perpetually nervous.
    When they spot a player, they inflate their bodies and float away to safety.
    Their lightweight bodies make them difficult to capture and fast enough to evade most threats.
    """

    def __init__(self, x=60, y=17):
        super().__init__(x, y)
        self.movement.set_state(es.CowardlyEnemyState())

    def get_icon(self):
        return "P"

    def get_name(self):
        return "Panic Puffs"

    def enemy_experience(self) -> int:
        return 100


"""
SciFi Enemies
"""


class CyborgChainsaw(Enemy):
    """
    Cyborg Chainsaw: A menacing, half-machine, half-monster hybrid equipped with razor-sharp chainsaws for limbs.
    It relentlessly pursues its prey, tearing through anything that stands in its path.
    """

    def __init__(self, x=60, y=17):
        super().__init__(x, y)
        self.movement.set_state(es.AggressiveEnemyState())

    def get_icon(self):
        return "W"

    def get_name(self):
        return "Cyborg Chainsaw"

    def enemy_experience(self) -> int:
        return 2


class PoisonousMold(CloneableEnemy):
    """
    PoisonousMold
    """

    def __init__(self, x=60, y=17):
        super().__init__(x, y)
        self.health = 100
        self.power = 1
        self.movement.set_state(es.PassiveAttackEnemyState())
        self.cloning_probability = 0.5

    def get_icon(self):
        return "L"

    def get_name(self):
        return "Poisonous Mold"

    def enemy_experience(self) -> int:
        return 2

    def clone(self, coordinates=None):
        if coordinates is None:
            coordinates = self.coordinates
        new_laser_shark = copy.deepcopy(self)
        new_laser_shark.coordinates = coordinates
        return new_laser_shark

    def update(self, game_state) -> Coordinates:
        new_coordinates = super().update(game_state)
        if random.random() < self.cloning_probability:
            x, y = self.coordinates
            available_position = []
            game_map = game_state.game_map
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if i == j == 0:
                        continue
                    if game_map.get_object_at(x + i, y + j).get_icon() == " ":
                        available_position.append(Coordinates(x + i, y + j))
            if available_position:
                self.cloning_probability = self.cloning_probability * 0.5
                copy_laser_shark = self.clone(
                    available_position[random.randint(0, len(available_position)) - 1]
                )
                game_state.game_map.get_enemies().add(copy_laser_shark)
        return new_coordinates


class BioShields(Enemy):
    """
    Bio-Shields: These living, organic walls are composed of highly resistant biomatter.
    They remain stationary, providing a barrier for other creatures or valuable resources.
    When attacked, they release spores that repair the damage and deter further aggression.
    """

    def __init__(self, x=60, y=17):
        super().__init__(x, y)
        self.movement.set_state(es.PassiveEnemyState())

    def get_icon(self):
        return "B"

    def get_name(self):
        return "Bio-Shields"

    def enemy_experience(self) -> int:
        return 2


class Cryonites(Enemy):
    """
    Cryonites: These fragile, crystalline beings are made of an ice-like substance that shatters easily.
    They are highly sensitive to heat and flee from any player exuding warmth or wielding heat-based weapons.
    """

    def __init__(self, x=60, y=17):
        super().__init__(x, y)
        self.movement.set_state(es.CowardlyEnemyState())

    def get_icon(self):
        return "Y"

    def get_name(self):
        return "Cautious One"

    def enemy_experience(self) -> int:
        return 100
