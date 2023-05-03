from state.hero import Hero
from state.game_map import GameMap, Room


class State:
    def __init__(self, hero: Hero):
        # GameMap
        self.game_map: GameMap = GameMap(Room("0"), 1)

        # Player
        self.hero = hero

        # Additional global state
        self.lives = 5
        self.score = 0
        self.room_changed = False
        self.current_level = 1
