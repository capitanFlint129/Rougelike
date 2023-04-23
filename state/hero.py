from state.actor import Actor


class Hero(Actor):
    def __init__(self):
        super().__init__()
        self.power = 5

    def get_icon(self):
        return "O"

    def get_name(self):
        return "hero"
