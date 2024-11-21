from abc import ABC, abstractmethod

class AbstractAgen(ABC):
    @abstractmethod
    def play(x, y, human_count, humans, zombie_count, zombies):
        pass