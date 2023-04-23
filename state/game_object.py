from abc import ABC, abstractmethod


class GameObject(ABC):
    @abstractmethod
    def get_icon(self):
        pass

    @abstractmethod
    def get_name(self):
        pass
