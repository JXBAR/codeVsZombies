import sys
sys.path.append(sys.path[0] + "/..")

from simulation.simulation import Simulation
from simulation.agen_closest_zombie import ClosestZombieAgen

level_file = 'data/levels/simple.txt'
with open(level_file, 'r') as file:
    lines = file.readlines()
print(lines)
agen = ClosestZombieAgen()
sim = Simulation(lines, agen)

while not sim.finished:
    sim.tick()
    print(sim.states[sim.round])
 