from abc import ABC

from game_engine.inventory_menu.menu_state import MenuState


class MenuCommand(ABC):
    def execute(self, menu_state: MenuState):
        pass


class MenuCommandUp(MenuCommand):
    def execute(self, menu_state: MenuState):
        menu_state.user_position = max(0, menu_state.user_position - 1)


class MenuCommandDown(MenuCommand):
    def execute(self, menu_state: MenuState):
        menu_state.user_position = min(
            len(menu_state.items_list) - 1, menu_state.user_position + 1
        )


class MenuCommandApply(MenuCommand):
    def execute(self, menu_state: MenuState):
        if len(menu_state.items_list) > 0:
            current_item = menu_state.items_list[menu_state.user_position]
            if current_item in menu_state.equipped:
                menu_state.hero.unequip(current_item)
            else:
                menu_state.hero.equip(current_item)


class MenuCommandClose(MenuCommand):
    def execute(self, menu_state: MenuState):
        menu_state.is_open = False
