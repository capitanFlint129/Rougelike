from abc import ABC

from state.game_object import GameObject
from state.item import Item


class Actor(GameObject, ABC):
    def __init__(self):
        self.inventory: [Item] = []
        self.equipped: [Item] = []
        self.health = 0
        self.power = 0

    def attack(self, actor: "Actor"):
        power = self.power + sum([item.attack_bonus() for item in self.equipped])
        actor.get_damage(power)

    def get_item(self, item: Item):
        self.inventory.append(item)

    def equip(self, item: Item):
        self.equipped.append(item)

    def get_damage(self, damage):
        armor = sum([item.armor_bonus() for item in self.equipped])
        damage = max(0, damage - armor)
        self.health = max(0, self.health - damage)
