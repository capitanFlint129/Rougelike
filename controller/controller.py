from abc import ABC, abstractmethod

from state.state import State


class Controller(ABC):
    @abstractmethod
    def update_state(self, game_state: State):
        pass
