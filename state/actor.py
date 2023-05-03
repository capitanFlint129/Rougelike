from abc import ABC
from typing import Set

from state.game_object import GameObject
from state.item import Item
from utils.coordinates import Coordinates


class Actor(GameObject, ABC):
    def __init__(self, x, y):
        self.inventory: Set[Item] = set()
        self.equipped: Set[Item] = set()
        self.health = 10
        self.power = 1
        self.is_alive = True
        self.coordinates = Coordinates(x, y)

    def attack(self, actor: "Actor"):
        power = self.power + sum([item.attack_bonus() for item in self.equipped])
        actor.get_damage(power)

    def get_item(self, item: Item):
        self.inventory.add(item)

    def equip(self, item: Item):
        self.equipped.add(item)

    def unequip(self, item: Item):
        self.equipped.remove(item)

    def get_damage(self, damage):
        armor = sum([item.armor_bonus() for item in self.equipped])
        damage = max(0, damage - armor)
        self.health = max(0, self.health - damage)
        if self.health == 0:
            self.is_alive = False

    def __str__(self):
        return self.get_icon()

    def get_x(self):
        return self.coordinates.x

    def get_y(self):
        return self.coordinates.y

    def set_x(self, x):
        self.coordinates.x = x

    def set_y(self, y):
        self.coordinates.y = y

    def move_to(self, x, y):
        self.coordinates.x = x
        self.coordinates.y = y
