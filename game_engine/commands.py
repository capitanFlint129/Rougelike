from abc import ABC

from state.state import State


class GameEngineCommand(ABC):
    def execute(self, state: State):
        pass


class OpenInventoryCommand(GameEngineCommand):
    def __init__(self, inventory_menu):
        self.inventory_menu = inventory_menu

    def execute(self, state: State):
        if state.lives != 0:
            self.inventory_menu.open()


class OkCommand(GameEngineCommand):
    def execute(self, state: State):
        pass
