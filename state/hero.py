from state.actor import Actor, Coordinates


class Hero(Actor):
    def __init__(self, x=6, y=3):
        super(Hero, self).__init__(x, y)
        self.power = 5

    def get_icon(self):
        return "O"

    def get_name(self):
        return "hero"
