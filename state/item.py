from abc import abstractmethod

from state.game_object import GameObject


class Item(GameObject):
    @abstractmethod
    def attack_bonus(self):
        pass

    @abstractmethod
    def armor_bonus(self):
        pass


class Sword(Item):
    def get_icon(self):
        return "|"

    def get_name(self):
        return "Iron sword"

    def attack_bonus(self):
        return 10

    def armor_bonus(self):
        return 0


class Shield(Item):
    def get_icon(self):
        return "["

    def get_name(self):
        return "Iron shield"

    def attack_bonus(self):
        return 0

    def armor_bonus(self):
        return 10
