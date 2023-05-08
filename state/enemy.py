from state.actor import Actor
from state.item import Item
from utils.coordinates import Coordinates
import state.enemy_strategy as es


class Enemy(Actor):
    """
    Represents an enemy character within a game. Inherits from the Actor class, and overrides the "get_icon" and
    "get_name" methods to provide the enemy's visual representation and name. The class also overrides the "equip" and
    "get_item" methods to prevent the enemy from equipping or picking up items.
    """

    def __init__(self, x=60, y=17):
        super(Enemy, self).__init__(x, y)
        self.movement_strategy = es.EnemyMovement()

    def get_icon(self):
        return "*"

    def get_name(self):
        return "enemy"

    def equip(self, item: Item):
        pass

    def get_item(self, item: Item):
        pass

    def enemy_experience(self) -> int:
        pass

    def move(self, game_state) -> Coordinates:
        player_coordinates = game_state.hero.coordinates
        return self.movement_strategy.move(self.coordinates, player_coordinates)


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
        self.movement_strategy.set_strategy(es.AggressiveEnemyStrategy())

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


class PanicPuffs(Enemy):
    """
    Panic Puffs: These round, fluffy creatures are reminiscent of cotton balls and are perpetually nervous.
    When they spot a player, they inflate their bodies and float away to safety.
    Their lightweight bodies make them difficult to capture and fast enough to evade most threats.
    """

    def __init__(self, x=60, y=17):
        super().__init__(x, y)
        self.movement_strategy.set_strategy(es.CowardlyEnemyStrategy())

    def get_icon(self):
        return "P"

    def get_name(self):
        return "Panic Puffs"

    def enemy_experience(self) -> int:
        return 1


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
        self.movement_strategy.set_strategy(es.AggressiveEnemyStrategy())

    def get_icon(self):
        return "W"

    def get_name(self):
        return "Cyborg Chainsaw"

    def enemy_experience(self) -> int:
        return 2


class LaserShark(Enemy):
    """
    Laser Shark: An advanced, genetically-engineered shark armed with laser weaponry on its dorsal fin.
    It aggressively hunts down any intruders in its territory, unleashing devastating energy beams to subdue its prey.
    """

    def __init__(self, x=60, y=17):
        super().__init__(x, y)
        self.movement_strategy.set_strategy(es.AggressiveEnemyStrategy())

    def get_icon(self):
        return "L"

    def get_name(self):
        return "Laser Shark"

    def enemy_experience(self) -> int:
        return 2


class BioShields(Enemy):
    """
    Bio-Shields: These living, organic walls are composed of highly resistant biomatter.
    They remain stationary, providing a barrier for other creatures or valuable resources.
    When attacked, they release spores that repair the damage and deter further aggression.
    """

    def __init__(self, x=60, y=17):
        super().__init__(x, y)
        self.movement_strategy.set_strategy(es.PassiveEnemyStrategy())

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
        self.movement_strategy.set_strategy(es.CowardlyEnemyStrategy())

    def get_icon(self):
        return "Y"

    def get_name(self):
        return "Cautious One"

    def enemy_experience(self) -> int:
        return 1
