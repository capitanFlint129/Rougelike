from state.hero import Hero


class State:
    def __init__(self, hero: Hero):
        self.rows_number = 26
        self.level = []
        self.enemies = []
        self.hero = hero
        self.enemy_x = 65
        self.enemy_y = 20
        self.e_last_x = self.enemy_x
        self.e_last_y = self.enemy_y
        self.player_x = 6
        self.player_y = 3
        self.last_x = 6
        self.last_y = 3
        self.lives = 5
        self.score = 0
        self.level_changed = False
        self.current_level = 1
