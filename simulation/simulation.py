from  .agent import AbstractAgen
import copy
import math

class Simulation():
    def __init__(self, levelData, agen: AbstractAgen):
        self.states = []
        self.round = 0
        self.score = 0
        self.agen = agen
        self.finished = False
        self.victory = False
        self.loadLevel(levelData);
        self.saveState()
    def loadLevel(self, lines):
        self.player_x, self.player_y = map(int, lines[0].strip().split())
        self.human_count =  int(lines[1].strip());
        self.humans = []
        for i in range(self.human_count):
            human_id, human_x, human_y = map(int, lines[2 + i].strip().split())
            self.humans.append({
                    "type": "human",
                    "id": human_id,
                    "x":  human_x,
                    "y": human_y
            })
        self.zombie_count = int(lines[2 + self.human_count].strip())
        self.zombies = []
        for i in range(self.zombie_count):
            values = lines[3 + self.human_count + i].strip().split()
            zombie_id, zombie_x, zombie_y, zombie_nx, zombie_ny = map(int, values)
            self.zombies.append({
                    "type": "zombie",
                    "id": zombie_id,
                    "x":  zombie_x,
                    "y": zombie_y,
                    "nx": zombie_nx,
                    "ny": zombie_ny
            })

    def saveState(self):
        state = {
            "round": self.round,
            "score": self.score,
            "finished": self.finished,
            "victory": self.victory,
            "player": {
                "type": "player",
                "x": self.player_x,
                "y": self.player_y
            },
            "human_count": self.human_count,
            "humans": self.humans.copy(),
            "zombie_count": self.zombie_count,
            "zombies": self.zombies.copy()
        }
        self.states.append(state)
    
    @staticmethod 
    def distanceEuclidienne(x1, y1, x2, y2):
        return math.sqrt( (x2 - x1)**2 + (y2 - y1)**2)
   
    @staticmethod
    def move(x1, y1, x2, y2, units: int):
        norme = math.sqrt( (x2 - x1)**2 + (y2 - y1)**2)
        if norme == 0:
            return {'x': x1, 'y': y1}

        if units >= norme:
            return {'x': x2, 'y': y2}
        
        return {
            'x': int(x1 + units * (x2 - x1) / norme),
            'y': int(y1 + units * (y2 - y1) / norme)
        }

    @staticmethod
    def fibonacci(n):
        if n <= 0:
            return 0
        elif n == 1:
            return 1
        a, b = 0, 1
        for _ in range(2, n + 1):
            a, b = b, a + b
        return b

    def calculate_score(self, zombies_killed_count):
        humans_alive = self.human_count
        score = 0
        for i in range(1, zombies_killed_count + 1):
            zombie_value = humans_alive ** 2 * 10
            fibonacci_term = self.fibonacci(i + 2)
            score += zombie_value * fibonacci_term
        return score
    
    def tick(self):
        if(self.finished):
            return True
        target = self.agen.play(
            self.player_x,
            self.player_y,
            self.human_count,
            copy.deepcopy(self.humans),
            self.zombie_count,
            copy.deepcopy(self.zombies)
        )

        for zombie in self.zombies:
            zombie['x'] = zombie['nx']
            zombie['y'] = zombie['ny']
            dist = self.distanceEuclidienne(zombie['x'], zombie['y'], self.player_x, self.player_y)
            print('dist', dist)
            closestHuman = None
            closestDist = float('inf')
            humans = self.humans + [{"x": self.player_x, "y": self.player_y}]
            for human in humans:
                dist = math.sqrt( (zombie['x'] - human['x'])**2 + (zombie['y'] - human['y'])**2)
                if dist < closestDist:
                    closestDist = dist
                    closestHuman = human
            nextPos = self.move(zombie['x'], zombie['y'], closestHuman['x'], closestHuman['y'], 400)
            zombie['nx'] = nextPos['x']
            zombie['ny'] = nextPos['y']

        nextPos = self.move(self.player_x, self.player_y, target['target_x'], target['target_y'], 1000)
        self.player_x = nextPos['x']
        self.player_y = nextPos['y']

      
        self.zombies = [item for item in self.zombies if self.distanceEuclidienne(item['x'], item['y'], self.player_x, self.player_y) >= 2000]
        zombies_killed_count = self.zombie_count - len(self.zombies)   
        self.score += self.calculate_score(zombies_killed_count)

        self.zombie_count = len(self.zombies)

        def isHumanEaten(human):
            for zombie in self.zombies:
                if (zombie['x'] == human['x']) and (zombie['y'] == human['y']):
                    return True
            return False

        self.humans = [item for item in self.humans if not isHumanEaten(item)]
        self.human_count = len(self.humans)

        self.round = self.round + 1

        if(self.human_count == 0):
            self.finished = True
            self.victory = False
            self.saveState()
            return True
    
        if(self.zombie_count == 0):
            if(self.human_count > 0):
                self.finished = True
                self.victory = True
                self.saveState()
                return True
        
        self.saveState()
        return False

