from abc import ABC, abstractmethod

class Drawable(ABC):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @abstractmethod
    def draw(self, screen, camera):
        pass
