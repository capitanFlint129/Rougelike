from game_object import GameObject


class Wall(GameObject):
    def get_icon(self):
        return "#"

    def get_name(self):
        return "wall"


class Door(GameObject):
    def get_icon(self):
        return " "

    def get_name(self):
        return "door"


class Coin(GameObject):

    def get_icon(self):
        return "c"

    def get_name(self):
        return "coin"


class FreeSpace(GameObject):
    def get_icon(self):
        return ""

    def get_name(self):
        return "free space"


class MapBorder(GameObject):
    def get_icon(self):
        return "_"

    def get_name(self):
        return "border"


class Thorn(GameObject):
    def __init__(self, icon: str):
        super().__init__()
        self.icon = icon

    def get_name(self):
        pass

    def get_icon(self):
        return


class ExitPortal(GameObject):
    def get_icon(self):
        return "+"

    def get_name(self):
        return "portal to the next level"
