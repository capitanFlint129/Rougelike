import random
from abc import ABC

from state.enemy import Actor
from utils.coordinates import Coordinates


class ActorDecorator(Actor, ABC):
    def __init__(self, decorated_actor: Actor):
        super().__init__(0, 0)
        self.decorated_actor = decorated_actor

    def get_icon(self):
        return super().get_icon()

    def update(self, game_state) -> Coordinates:
        return super().update(game_state)

    def get_decorated_actor(self):
        return self.decorated_actor


class ConfusedActorDecorator(ActorDecorator, ABC):
    def get_icon(self):
        return "z"

    def get_name(self):
        return self.decorated_actor.get_name()

    def update(self, game_state) -> Coordinates:
        dx = random.randint(-1, 1)
        dy = random.randint(-1, 1)
        return Coordinates(self.coordinates.x + dx, self.coordinates.y + dy)
