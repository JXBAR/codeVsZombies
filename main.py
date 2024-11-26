import pygame
import sys
from simulation.simulation import Simulation
from simulation.dummy_agen import DummyAgen
from simulation.agen_closest_zombie import ClosestZombieAgen
import math
from info_display import InfoDisplay


# Lire le fichier de niveau 
level_file = 'data/levels/chaos.txt'
with open(level_file, 'r') as file:
    lines = file.readlines()

agen = ClosestZombieAgen()
sim = Simulation(lines, agen)

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

# Police pour le texte
font = pygame.font.Font(None, 20)

view = {
    'offset_x': int(screen_width * 271 / 1920),
    'offset_y': int(screen_height * 138 / 1080),
    'xe': int(screen_width * 1637 / 1920),
    'ye': int(screen_height * 138 / 1080),
    'width': int(screen_width * 1366 / 1920),
    'height': int(screen_height * 768 / 1080),
    'world_width': 16000,
    'world_heigth' : 9000,
    'unit2px':   screen_width * 1366 / 1920  /16000
 }

print(view)
def coordinateToPx(view, x, y):
    return {
        "x" : int(view['offset_x'] + (x * view['width'] / view['world_width'])),
        "y" : int(view['offset_y'] + (y * view['height'] / view['world_heigth']))
    }

printedState = 0
state = sim.states[sim.round]
running = True

background_image = pygame.image.load('data/assets/background_clean.jpg')
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))
soldierImg = pygame.image.load('data/assets/soldier/soldier_torso_2h.png')
infoDisplay = InfoDisplay()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                sim.tick()
                if sim.round == 1:
                    printedState = 0
                elif printedState >= sim.round:
                    printedState = sim.round
                else:
                    printedState = printedState + 1
                    state = sim.states[printedState]

                print(state)

    mouse_x, mouse_y = pygame.mouse.get_pos()
    screen.blit(background_image, (0, 0))

    # Dessiner les bordures du monde
    pygame.draw.rect(screen, white, (coordinateToPx(view, 0, 0)['x'] , coordinateToPx(view, 0, 0)['y'],  view['width'],  view['height']), 5)

    statePlayer = 0
    animated = 0

    # Dessiner les objets dessinables
    drawables = [state['player']] + state['humans'] + state['zombies']

    for drawable in drawables:
        coord = coordinateToPx(view,  drawable['x'],  drawable['y'])
        if drawable['type'] == 'player':
            pygame.draw.circle(
                screen,
                (186,142,35),
                (int(coord['x']),int(coord['y'])),
                int(2000 * view['unit2px']),
                2
            )

            player_rect = soldierImg.get_rect(center=(coord['x'], coord['y']) )
            dx = mouse_x - player_rect.centerx
            dy = mouse_y  - player_rect.centery
            angle = math.degrees(math.atan2(dy, dx)) + 90

            orientation = 0

            if printedState + 1 <= sim.round:
                nextStateIndex = printedState + 1
                nextState = sim.states[nextStateIndex]
                nextPlayerCoord = coordinateToPx(view , nextState['player']['x'], nextState['player']['y'])
                orientation = math.degrees(
                    math.atan2(
                        - coord['y'] + nextPlayerCoord['y'],
                        - coord['x'] + nextPlayerCoord['x'],
                    )
                )   + 90
                pygame.draw.circle(
                    screen,
                    (186,142,35),
                    (int(nextPlayerCoord['x']),int(nextPlayerCoord['y'])),
                    int(100 * view['unit2px'])
                )
         
            rotated_image = pygame.transform.rotate(soldierImg, -orientation)
            rotated_rect = rotated_image.get_rect(center=player_rect.center)
            screen.blit( rotated_image, rotated_rect.topleft)

            # pygame.draw.line(screen, (255, 0, 0), player_rect.center, (mouse_x, mouse_y), 2)
        elif drawable['type'] == 'human':
            pygame.draw.circle(
                screen,
                (235, 16, 47),
                (int(coord['x']),int(coord['y'])),
                int(50 * view['unit2px'])
            )
            pygame.draw.circle(
                screen,
                (186,142,35),
                (int(coord['x']),int(coord['y'])),
                int(400 * view['unit2px']),
                2
            )
        elif drawable['type'] == 'zombie':
            pygame.draw.circle(
                screen,
                (255,222,33),
                (int(coord['x']),int(coord['y'])),
                int(50 * view['unit2px'])
                )
            pygame.draw.circle(
                screen, (86,142,35),
                (int(coord['x']),int(coord['y'])),
                int(400 * view['unit2px']),
                2)

    player_position = f"Player position: ({state['player']['x']}, {state['player']['y']})"
    human_count = f"Human counts: {len(state['humans'])}"
    infoDisplay.store(0, 'Round', f"{state['round']} / {sim.round}")
    infoDisplay.store(1, 'Score', f"{state['score']}")
    infoDisplay.store(2, 'Player', f"({state['player']['x']}, {state['player']['y']})")
    infoDisplay.store(3, 'Zombies', f"({state['zombie_count']})")
    infoDisplay.store(10,"PRESS SPACE TO RUN", '')

    result = ' - '
    if(state['finished']):
        result = 'VICTORY' if state['victory'] else 'DEFEAT'
    
    infoDisplay.store(4, 'Result', result)

    infoDisplay.draw(screen, font, view['xe'] + 10, view['offset_y'] + 20,  white)
    pygame.display.flip()
    pygame.time.Clock().tick(30)

# Quitter Pygame
pygame.quit()
sys.exit()
