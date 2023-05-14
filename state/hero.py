from typing import List
from state.actor import Actor
from state.enemy import Enemy
import state.ability as abilities


class Hero(Actor):
    """
    A player-controlled character in the game

    Attributes:
        x (int): The x-coordinate of the hero's current position.
        y (int): The y-coordinate of the hero's current position.
        health (int): The hero's current health points.
        is_alive (bool): True if the hero is currently alive, False otherwise.
        experience (int): The amount of experience points the hero has accumulated.
        power (int): The hero's current attack power.
        abilities (List[abilities.Ability]): A list of abilities that the hero has.
    """

    def __init__(self, x=6, y=3):
        """
        Initializes a new instance of the Hero class.

        Args:
            x (int): The x-coordinate of the hero's initial position. Default: 6.
            y (int): The y-coordinate of the hero's initial position. Default: 3.
        """
        super(Hero, self).__init__(x, y)
        self.experience = 0
        self.power = 2
        self.abilities: List[abilities.Ability] = []
        self.abilities.append(abilities.ConfuseAbility(self))

    def get_icon(self) -> str:
        """
        Returns the character icon representing the hero.

        Returns:
            str: The character icon representing the hero.
        """
        return "O"

    def get_name(self) -> str:
        """
        Returns the name of the hero.

        Returns:
            str: The name of the hero.
        """
        return "hero"

    def attack(self, actor: "Actor"):
        """
        Attacks the specified actor, reducing their health points.

        Args:
            actor (Actor): The actor to attack.
        """
        super().attack(actor)
        if isinstance(actor, Enemy) and not actor.is_alive:
            self.get_experience(actor.enemy_experience())
        else:
            for ability in self.abilities:
                ability.spell_ability(actor)

    def get_experience(self, exp: int):
        """
        Adds the specified amount of experience points to the hero's current experience.

        Args:
            exp (int): The amount of experience points to add.
        """
        self.experience += exp
        if self.experience == 2:
            self.experience = 0
            self.health = 10
            self.power += 1

    def resurrect_player(self):
        """
        Restores the hero's health and sets is_alive to True.
        """
        self.health = 10
        self.is_alive = True
        self.inventory = set()
        self.equipped = set()
