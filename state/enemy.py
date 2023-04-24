from state.actor import Actor
from state.item import Item


class Enemy(Actor):
    # def __init__(self):
    #     super().__init__()
    #     self.power = 10

    def get_icon(self):
        return "*"

    def get_name(self):
        return "enemy"

    def equip(self, item: Item):
        pass

    def get_item(self, item: Item):
        pass
