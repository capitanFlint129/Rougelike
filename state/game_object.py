from abc import ABC, abstractmethod


class GameObject(ABC):
    @abstractmethod
    def get_icon(self):
        pass

    @abstractmethod
    def get_name(self):
        pass

    def __str__(self):
        return self.get_icon()
