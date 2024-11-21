import pygame
import sys
from human import Human
from zombie import Zombie
from player import Player
from camera import Camera
from simulation.simulation import Simulation
from simulation.dummy_agen import DummyAgen
# Initialiser Pygame
pygame.init()

# Définir les dimensions de la fenêtre
screen_width = 1600
screen_height = 900

# Créer la fenêtre
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Simulation Caméra Pygame")

# Définir les couleurs
white = (255, 255, 255)
black = (0, 0, 0)
gray = (200, 200, 200)

# Définir les dimensions du monde
world_width = 16000
world_height = 9000

# Taille des carrés de la grille
grid_size = 100

# Position initiale de la caméra
camera_speed = 10

# Police pour le texte
font = pygame.font.Font(None, 17)



# Lire le fichier de niveau ee
level_file = 'simple.txt'
with open(level_file, 'r') as file:
    lines = file.readlines()


agen = DummyAgen()
sim = Simulation(lines, agen)
state = sim.states[sim.round]
# Initialiser la caméra centrée sur le joueur
camera = Camera(state['player']['x'] - screen_width // 2,state['player']['y']  - screen_height // 2)
 # Calculer le zoom pour voir toute la carte
zoom_width =    (world_width + 5000) / screen_width
zoom_height =   (world_height + 2000) / screen_height
camera.zoom = min(zoom_width, zoom_height)

# Variables pour le déplacement de la caméra avec la souris
mouse_dragging = False
last_mouse_pos = None
# Boucle principale
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:  # Roulette vers le haut
                camera.zoom /= 1.1
            elif event.button == 5:  # Roulette vers le bas
                camera.zoom *= 1.1
            elif event.button == 3:  # Clic droit enfoncé
                mouse_dragging = True
                last_mouse_pos = event.pos
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 3:  # Clic droit relâché
                mouse_dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if mouse_dragging:
                dx = event.pos[0] - last_mouse_pos[0]
                dy = event.pos[1] - last_mouse_pos[1]
                camera.x -= dx * camera.zoom
                camera.y -= dy * camera.zoom
                last_mouse_pos = event.pos
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                sim.tick()
                state = sim.states[sim.round]
 
    # Limiter la caméra aux bords du monde
    camera.x = max(-1000, min(camera.x, world_width - screen_width / camera.zoom))
    camera.y = max(-1000, min(camera.y, world_height - screen_height / camera.zoom))

    # Remplir l'écran avec une couleur
    screen.fill(white)

    # Dessiner la grille en damier
    for x in range(0, world_width, grid_size):
        for y in range(0, world_height, grid_size):
            if (x // grid_size + y // grid_size) % 2 == 0:
                color = white
            else:
                color = gray
            pygame.draw.rect(screen, color, (int((x - camera.x) / camera.zoom), int((y - camera.y) / camera.zoom), int(grid_size / camera.zoom), int(grid_size / camera.zoom)))

    # Dessiner les bordures du monde
    pygame.draw.rect(screen, (255, 0, 0), (int((0 - camera.x) / camera.zoom), int((0 - camera.y) / camera.zoom), int(world_width / camera.zoom), int(world_height / camera.zoom)), 5)
    
   

    # Dessiner les objets dessinables
    drawables = [state['player']] + state['humans'] + state['zombies']

    for drawable in drawables:
        if drawable['type'] == 'player':
            pygame.draw.circle(screen, (0, 0, 255), (int(( drawable['x'] - camera.x) / camera.zoom), int(( drawable['y'] - camera.y) / camera.zoom)), int(50 / camera.zoom))
            pygame.draw.circle(screen, (186,142,35), (int(( drawable['x'] - camera.x) / camera.zoom), int(( drawable['y'] - camera.y) / camera.zoom)), int(2000 / camera.zoom), 2)
        elif drawable['type'] == 'human':
            pygame.draw.circle(screen, (235, 16, 47), (int((drawable['x']  - camera.x) / camera.zoom), int((drawable['y']  - camera.y) / camera.zoom)), int(50 / camera.zoom))
            pygame.draw.circle(screen, (186,142,35), (int((drawable['x']  - camera.x) / camera.zoom), int((drawable['y']  - camera.y) / camera.zoom)), int(400 / camera.zoom), 2)
        elif drawable['type'] == 'zombie':
            pygame.draw.circle(screen, (255,222,33), (int((drawable['x']  - camera.x) / camera.zoom), int((drawable['y']  - camera.y) / camera.zoom)), int(50 / camera.zoom))
            pygame.draw.circle(screen, (86,142,35), (int((drawable['x']  - camera.x) / camera.zoom), int((drawable['y']  - camera.y) / camera.zoom)), int(400 / camera.zoom), 2)

    # Afficher la position de la caméra avec le zoom inversé et arrondi à deux chiffres après la virgule
    inverse_zoom = 1 / camera.zoom
    camera_text = font.render(f"Cam: {round(camera.x)}:{round(camera.y)}, z:{inverse_zoom:.2f}", True, black)
    screen.blit(camera_text, (screen_width - camera_text.get_width() - 10, 10))


    # Obtenir la position de la souris sur l'écran
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Convertir la position de la souris en coordonnées du monde
    world_mouse_x = camera.x + mouse_x * camera.zoom
    world_mouse_y = camera.y + mouse_y * camera.zoom

    # Arrondir les coordonnées à l'entier supérieur
    world_mouse_x_ceil = int(world_mouse_x) + 1
    world_mouse_y_ceil = int(world_mouse_y) + 1

    # Afficher la position de la souris dans les coordonnées du monde
    mouse_text = font.render(f"Mouse: {world_mouse_x_ceil}:{world_mouse_y_ceil}", True, black)
    screen.blit(mouse_text, (screen_width - mouse_text.get_width() - 10, 10 + camera_text.get_height()))

    # Mettre à jour l'affichage
    pygame.display.flip()

    # Contrôler la vitesse de la boucle
    pygame.time.Clock().tick(30)

# Quitter Pygame
pygame.quit()
sys.exit()
