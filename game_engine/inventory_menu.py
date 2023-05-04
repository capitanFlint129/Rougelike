import time

from gui.command_handler import CommandHandler, UserCommand


class InventoryMenu:
    """
    A class that manages the inventory menu, allowing the user to interact with their inventory.

    The inventory menu displays the items in the player's inventory and allows them to equip and
    unequip items. The menu can be opened and closed with a specific key command, which is handled
    by the command_handler instance.
    """

    def __init__(self, state, gui, command_handler: CommandHandler):
        self.state = state
        self.gui = gui
        self.command_handler = command_handler

    def open(self):
        user_position = 0
        items_list = list(self.state.hero.inventory)
        self.gui.print_inventory(self.state, items_list, user_position)
        time.sleep(0.2)
        while True:
            user_command = self.command_handler.get_command()
            if len(items_list) > 0:
                current_item = items_list[user_position]
                if user_command == UserCommand.UP:
                    user_position = max(0, user_position - 1)
                elif user_command == UserCommand.DOWN:
                    user_position = min(len(items_list) - 1, user_position + 1)
                elif user_command == UserCommand.APPLY:
                    if current_item in self.state.hero.equipped:
                        self.state.hero.unequip(current_item)
                    else:
                        self.state.hero.equip(current_item)
            if user_command == UserCommand.OPEN_INVENTORY:
                break
            if user_command is not None:
                self.gui.print_inventory(self.state, items_list, user_position)
            time.sleep(0.1)
        self.gui.clear_inventory()
        time.sleep(0.1)
