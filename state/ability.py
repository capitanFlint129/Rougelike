import random

from state.actor import Actor
from events.event_handler import Event, EventHandler
from state.actor_decorator import ActorDecorator, ConfusedActorDecorator


class Ability:
    def __init__(self, owner: Actor):
        self.owner = owner

    def spell_ability(self, target: Actor):
        pass


class ConfuseAbility(Ability):
    def spell_ability(self, target: Actor):
        if isinstance(target, ConfusedActorDecorator):
            return

        proc = random.randint(0, 5)
        if proc != 0:
            return

        # wtf ?
        original_class = target.__class__
        target.__class__ = ConfusedActorDecorator

        def unconfuse_target():
            target.__class__ = original_class

        event = Event(unconfuse_target, [], 1)
        EventHandler.add_event(event)
