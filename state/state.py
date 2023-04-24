from state.hero import Hero


class State:
    def __init__(self, hero: Hero):
        self.rows_number = 26
        self.level = []
        self.enemies = []
        self.items = []
        self.exits_coordinates = []
        self.hero = hero
        self.player_x = 6
        self.player_y = 3
        self.last_x = 6
        self.last_y = 3
        self.lives = 5
        self.score = 0
        self.level_changed = False
        self.current_level = 1
