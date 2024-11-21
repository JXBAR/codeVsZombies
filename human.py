import pygame
from drawable import Drawable

class Human(Drawable):
    def __init__(self, x, y, id):
        super().__init__(x, y)
        self.id = id

    def draw(self, screen, camera):
        pygame.draw.circle(screen, (235, 16, 47), (int((self.x - camera.x) / camera.zoom), int((self.y - camera.y) / camera.zoom)), int(50 / camera.zoom))
        pygame.draw.circle(screen, (186,142,35), (int((self.x - camera.x) / camera.zoom), int((self.y - camera.y) / camera.zoom)), int(400 / camera.zoom), 2)