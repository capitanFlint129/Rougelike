from state.actor import Actor
from state.enemy import Enemy


class Hero(Actor):
    """
    Player
    """

    def __init__(self, x=6, y=3):
        super(Hero, self).__init__(x, y)
        self.experience = 0
        self.power = 5

    def get_icon(self):
        return "O"

    def get_name(self):
        return "hero"

    def attack(self, actor: "Actor"):
        super().attack(actor)
        if isinstance(actor, Enemy) and not actor.is_alive:
            self.get_experience(actor.enemy_experience())

    def get_experience(self, exp: int):
        self.experience += exp
        if self.experience == 2:
            self.experience = 0
            self.health = 10
            self.power += 1

    def resurrect_player(self):
        self.health = 10
        self.is_alive = True
