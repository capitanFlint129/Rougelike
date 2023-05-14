class MenuState:
    def __init__(self, hero, items_list, equipped, user_position=0):
        self.hero = hero
        self.items_list = items_list
        self.user_position = user_position
        self.equipped = equipped
        self.is_open = True
