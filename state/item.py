from abc import abstractmethod

from state.game_object import GameObject


class Item(GameObject):
    """
    The "Item" class is a subclass of "GameObject" that represents an item within the game.
    It is an abstract class that has abstract methods for obtaining the attack and armor bonuses of the item.
    """

    @abstractmethod
    def attack_bonus(self):
        pass

    @abstractmethod
    def armor_bonus(self):
        pass


class Sword(Item):
    """
    Me beat stronger!
    """

    def get_icon(self):
        return "|"

    def get_name(self):
        return "Iron sword"

    def attack_bonus(self):
        return 10

    def armor_bonus(self):
        return 0


class Shield(Item):
    """
    Me defend better!!
    """

    def get_icon(self):
        return "["

    def get_name(self):
        return "Iron shield"

    def attack_bonus(self):
        return 0

    def armor_bonus(self):
        return 10
