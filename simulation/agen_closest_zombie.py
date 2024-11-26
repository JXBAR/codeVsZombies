from agent import AbstractAgen
import math

class ClosestZombieAgen(AbstractAgen):
      def play(self, x, y, human_count, humans, zombie_count, zombies):
        for zombie in zombies:
          dist = self.distanceEuclidienne(x, y, zombie['x'], zombie['y'])
          zombie['dist'] = dist 
        
        zombiesSorted = sorted(zombies, key=lambda x: x['dist'])
        closest = zombiesSorted[0]
        return {
            "target_x": closest['x'],
            "target_y": closest['y'],
        }
      
      @staticmethod 
      def distanceEuclidienne(x1, y1, x2, y2):
        return math.sqrt( (x2 - x1)**2 + (y2 - y1)**2)