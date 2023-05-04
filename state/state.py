from state.hero import Hero
from state.game_map import GameMap, Room


class State:
    """
    Represents the current state of the game and is a key object for updating and passing data between objects.

    Attributes:
        game_map (GameMap): A "GameMap" object that represents the game's map.
        hero (Hero): A "Hero" object that represents the player.
        lives (int): The number of lives the player has.
        score (int): The current score of the player.
        room_changed (bool): A boolean that tracks whether the current room has changed.
        current_level (int): The current level of the game.
    """

    def __init__(self, hero: Hero):
        self.game_map: GameMap = GameMap(Room("0"), 1)
        self.hero: Hero = hero
        self.lives = 5
        self.score = 0
        self.room_changed = False
        self.current_level = 1
