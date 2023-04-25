from state.actor import Actor, Coordinates
from state.item import Item


class Enemy(Actor):
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
