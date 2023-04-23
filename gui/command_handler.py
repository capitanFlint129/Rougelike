from enum import Enum

import keyboard


class UserCommand(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4


class CommandHandler:
    @staticmethod
    def get_command() -> UserCommand:
        if keyboard.is_pressed("w"):
            return UserCommand.UP
        elif keyboard.is_pressed("s"):
            return UserCommand.DOWN
        elif keyboard.is_pressed("a"):
            return UserCommand.LEFT
        elif keyboard.is_pressed("d"):
            return UserCommand.RIGHT
        else:
            pass
