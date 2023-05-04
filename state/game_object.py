from abc import ABC, abstractmethod


class GameObject(ABC):
    """
    The "GameObject" class is an abstract base class that represents every object within the game map.
    The class has abstract methods for getting the object's icon and name, which are used to print the object.
    The class also has a string representation method that returns the object's icon.
    """

    @abstractmethod
    def get_icon(self):
        pass

    @abstractmethod
    def get_name(self):
        pass

    def __str__(self):
        return self.get_icon()
