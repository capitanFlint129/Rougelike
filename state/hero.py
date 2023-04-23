from state.actor import Actor


class Hero(Actor):
    def get_icon(self):
        return "O"

    def get_name(self):
        return "hero"
