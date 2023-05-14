import time

from game_engine.inventory_menu.menu_state import MenuState
from gui.command_handler import InventoryMenuCommandHandler


class InventoryMenu:
    """
    A class that manages the inventory menu, allowing the user to interact with their inventory.

    The inventory menu displays the items in the player's inventory and allows them to equip and
    unequip items. The menu can be opened and closed with a specific key command, which is handled
    by the command_handler instance.
    """

    def __init__(self, state, gui, command_handler: InventoryMenuCommandHandler):
        self.state = state
        self.gui = gui
        self.command_handler = command_handler

    def open(self):
        menu_state = MenuState(
            self.state.hero, list(self.state.hero.inventory), self.state.hero.equipped
        )
        self.gui.print_inventory(menu_state)
        time.sleep(0.2)
        while menu_state.is_open:
            command = self.command_handler.get_command()
            if command is not None:
                command.execute(menu_state)
                self.gui.print_inventory(menu_state)
            time.sleep(0.1)
        self.gui.clear_inventory()
        time.sleep(0.1)
