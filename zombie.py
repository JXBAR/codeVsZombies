import pygame
from drawable import Drawable

class Zombie(Drawable):
    def __init__(self, x, y, id):
        super().__init__(x, y)
        self.id = id

    def draw(self, screen, camera):
        # Dessiner un cercle vide avec une bordure de 1 pixel d'épaisseur
        pygame.draw.circle(screen, (255,222,33), (int((self.x - camera.x) / camera.zoom), int((self.y - camera.y) / camera.zoom)), int(50 / camera.zoom))
        pygame.draw.circle(screen, (186,142,35), (int((self.x - camera.x) / camera.zoom), int((self.y - camera.y) / camera.zoom)), int(400 / camera.zoom), 2)