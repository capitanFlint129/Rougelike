from state.hero import Hero
from generators.map_generator import Room


class State:
    def __init__(self, hero: Hero):
        # current GameMap - room with enemies and items.
        self.current_room: Room = Room("0")

        # Player
        self.hero = hero

        # Additional global state
        self.lives = 5
        self.score = 0
        self.room_changed = False
        self.current_level = 1
