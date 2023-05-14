import random

from state.actor import Actor
from events.event_handler import Event, EventHandler
from state.actor_decorator import ActorDecorator, ConfusedActorDecorator


class Ability:
    """
    Represents a generic ability that can be used by an actor in the game. An instance of this class should be created
    for each type of ability, and the "spell_ability" method should be implemented to define what the ability does.
    """

    def __init__(self, owner: Actor):
        """
        Initializes an ability object with an owner, which is the actor who possesses the ability.

        :param owner: the actor who possesses the ability
        """
        self.owner = owner

    def spell_ability(self, target: Actor):
        """
        This method should be implemented in a subclass to define what the ability does.

        :param target: the target actor or object of the ability
        """
        pass


class ConfuseAbility(Ability):
    """
    Represents an ability that confuses a target actor, causing it to move randomly instead of following its usual
    movement pattern. Inherits from the Ability class.
    """

    def spell_ability(self, target: Actor):
        """
        Confuses the target actor if it is not already confused. There is a 1 in 5 chance that the ability will fail
        to confuse the target. The target actor's class is temporarily changed to ConfusedActorDecorator, which causes
        it to move randomly instead of following its usual movement pattern.

        :param target: the target actor to be confused
        """
        if isinstance(target, ConfusedActorDecorator):
            return

        proc = random.randint(0, 5)
        if proc != 0:
            return

        original_class = target.__class__
        target.__class__ = ConfusedActorDecorator

        def unconfuse_target():
            target.__class__ = original_class

        event = Event(unconfuse_target, [], 1)
        EventHandler.add_event(event)
