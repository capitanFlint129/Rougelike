from typing import List

from state.actor import Actor
from state.enemy import Enemy
import state.ability as abilities
from state.item import Shield


class Hero(Actor):
    """
    Player
    """

    def __init__(self, x=6, y=3):
        super(Hero, self).__init__(x, y)
        self.experience = 0
        self.power = 2
        self.abilities: List[abilities.Ability] = []
        self.abilities.append(abilities.ConfuseAbility(self))

    def get_icon(self):
        return "O"

    def get_name(self):
        return "hero"

    def attack(self, actor: "Actor"):
        super().attack(actor)
        if isinstance(actor, Enemy) and not actor.is_alive:
            self.get_experience(actor.enemy_experience())
        else:
            for ability in self.abilities:
                ability.spell_ability(actor)

    def get_experience(self, exp: int):
        self.experience += exp
        if self.experience == 2:
            self.experience = 0
            self.health = 10
            self.power += 1

    def resurrect_player(self):
        self.health = 10
        self.is_alive = True
        self.inventory = set()
        self.equipped = set()
