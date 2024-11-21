import pygame
from drawable import Drawable

class Player(Drawable):
    def draw(self, screen, camera):
        pygame.draw.circle(screen, (0, 0, 255), (int((self.x - camera.x) / camera.zoom), int((self.y - camera.y) / camera.zoom)), int(50 / camera.zoom))
        pygame.draw.circle(screen, (186,142,35), (int((self.x - camera.x) / camera.zoom), int((self.y - camera.y) / camera.zoom)), int(2000 / camera.zoom), 2)