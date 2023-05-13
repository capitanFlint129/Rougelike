from abc import ABC
from game_engine.inventory_menu.menu_state import MenuState


class MenuCommand(ABC):
    """
    Base class for all menu commands. All menu commands should inherit from this class.
    """
    def execute(self, menu_state: MenuState):
        """
        Executes the command on the given menu state.

        Args:
            menu_state (MenuState): The current state of the menu.
        """
        pass


class MenuCommandUp(MenuCommand):
    """
    Command for moving the menu cursor up.
    """
    def execute(self, menu_state: MenuState):
        """
        Executes the menu cursor up command on the given menu state.

        Args:
            menu_state (MenuState): The current state of the menu.
        """
        menu_state.user_position = max(0, menu_state.user_position - 1)


class MenuCommandDown(MenuCommand):
    """
    Command for moving the menu cursor down.
    """
    def execute(self, menu_state: MenuState):
        """
        Executes the menu cursor down command on the given menu state.

        Args:
            menu_state (MenuState): The current state of the menu.
        """
        menu_state.user_position = min(
            len(menu_state.items_list) - 1, menu_state.user_position + 1
        )


class MenuCommandApply(MenuCommand):
    """
    Command for applying the selected item in the menu.
    """
    def execute(self, menu_state: MenuState):
        """
        Executes the apply item command on the given menu state.

        Args:
            menu_state (MenuState): The current state of the menu.
        """
        if len(menu_state.items_list) > 0:
            current_item = menu_state.items_list[menu_state.user_position]
            if current_item in menu_state.equipped:
                menu_state.hero.unequip(current_item)
            else:
                menu_state.hero.equip(current_item)


class MenuCommandClose(MenuCommand):
    """
    Command for closing the menu.
    """
    def execute(self, menu_state: MenuState):
        """
        Executes the close menu command on the given menu state.

        Args:
            menu_state (MenuState): The current state of the menu.
        """
        menu_state.is_open = False
