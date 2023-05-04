from state.actor import Actor, Coordinates
from state.item import Item


class Enemy(Actor):
    """
    Represents an enemy character within a game. Inherits from the Actor class, and overrides the "get_icon" and
    "get_name" methods to provide the enemy's visual representation and name. The class also overrides the "equip" and
    "get_item" methods to prevent the enemy from equipping or picking up items.
    """

    def __init__(self, x=60, y=17):
        super(Enemy, self).__init__(x, y)

    def get_icon(self):
        return "*"

    def get_name(self):
        return "enemy"

    def equip(self, item: Item):
        pass

    def get_item(self, item: Item):
        pass
